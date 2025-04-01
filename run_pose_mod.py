from estimater import *
from reader import *
import time
import argparse
from rename_files import rename_files


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    code_dir = os.path.dirname(os.path.realpath(__file__))
    parser.add_argument('--mesh_file', type=str, default=f'textured_simple.obj')
    parser.add_argument('--test_scene_dir', type=str, default=f'mustard')
    parser.add_argument('--est_refine_iter', type=int, default=5)
    parser.add_argument('--track_refine_iter', type=int, default=2)
    parser.add_argument('--debug', type=int, default=2)
    parser.add_argument('--debug_dir', type=str, default=f'{code_dir}/debug')
    parser.add_argument('--simulate', type=bool, default=False)
    args = parser.parse_args()

    set_logging_format()
    set_seed(0)

    scene_dir = f'{code_dir}/data/{args.test_scene_dir}'
    mesh_path = f'{code_dir}/data/{args.test_scene_dir}/mesh/{args.mesh_file}'

    rename_files(f'{scene_dir}/rgb', args.simulate)
    rename_files(f'{scene_dir}/depth', args.simulate)
    rename_files(f'{scene_dir}/masks', args.simulate)

    mesh = trimesh.load(mesh_path)

    debug = args.debug
    debug_dir = args.debug_dir
    os.system(f'rm -rf {debug_dir}/* && mkdir -p {debug_dir}/track_vis {debug_dir}/ob_in_cam')

    to_origin, extents = trimesh.bounds.oriented_bounds(mesh)
    bbox = np.stack([-extents/2, extents/2], axis=0).reshape(2,3)

    scorer = ScorePredictor()
    refiner = PoseRefinePredictor()
    glctx = dr.RasterizeCudaContext()
    est = FoundationPose(model_pts=mesh.vertices, model_normals=mesh.vertex_normals, mesh=mesh, scorer=scorer, refiner=refiner, debug_dir=debug_dir, debug=debug, glctx=glctx)
    logging.info("estimator initialization done")

    reader = DTwinReader(video_dir=scene_dir, shorter_side=None, zfar=np.inf)

    while not reader.get_video_detected():
        reader.get_first_frame()
    
    
    time_array = []
    pose_array = []

    while True:
        start_time = time.time()
        logging.info(f'i:{reader.get_count()}')
        color = reader.get_color()
        depth = reader.get_depth()
        if reader.get_count() == 0:
            mask = reader.get_mask().astype(bool)
            pose = est.register(K=reader.K, rgb=color, depth=depth, ob_mask=mask, iteration=args.est_refine_iter)

        else:
            pose = est.track_one(rgb=color, depth=depth, K=reader.K, iteration=args.track_refine_iter)
        
        #pose[0] = pose[5] = pose[10] = 1
        #pose[1] = pose[2] = pose[4] = pose[6] = pose[8] = pose[9] = 0 
        os.makedirs(f'{debug_dir}/ob_in_cam', exist_ok=True)
        # np.savetxt(f'{debug_dir}/ob_in_cam/frame{reader.get_count():06}.txt', pose.reshape(4,4))
        np.save(f'{debug_dir}/ob_in_cam/frame{reader.get_count():06}.npy', pose.reshape(4,4))

        center_pose = pose@np.linalg.inv(to_origin)
        vis = draw_posed_3d_box(reader.K, img=color, ob_in_cam=center_pose, bbox=bbox)
        vis = draw_xyz_axis(color, ob_in_cam=center_pose, scale=0.1, K=reader.K, thickness=3, transparency=0, is_input_rgb=True)
        
        os.makedirs(f'{debug_dir}/track_vis', exist_ok=True)
        imageio.imwrite(f'{debug_dir}/track_vis/frame{reader.get_count():06}.png', vis)
        
        elapsed_time = time.time() - start_time
        time_array.append(elapsed_time)

        reader.increment_count()
        
        if not reader.get_next_frame_exists():
            break
    
    f = open(f'{debug_dir}/timing.txt', "w")
    for i in time_array:
        f.write(f"{i}\n")
    f.close()
    