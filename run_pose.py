from estimater import *
from reader import *
import time
import argparse
from pathlib import Path
from mask_gen import create_mask
from rename_files import rename_files


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    code_dir = os.path.dirname(os.path.realpath(__file__))
    parser.add_argument('--test_scene_dir', type=str, default=f'box')
    parser.add_argument('--est_refine_iter', type=int, default=5)
    parser.add_argument('--track_refine_iter', type=int, default=2)
    parser.add_argument('--output_dir', type=str, default='output')
    parser.add_argument('--frame_output', type=bool, default=True)
    parser.add_argument('--simulation', type=bool, default=True)
    
    args = parser.parse_args()

    set_logging_format()
    set_seed(0)

    scene_dir = f'{code_dir}/data/{args.test_scene_dir}'
    print(scene_dir)
    mesh_folder = Path(f'{code_dir}/data/{args.test_scene_dir}/mesh/')
    
    obj_files = list(mesh_folder.glob("*.obj"))
    mesh_path = f'{obj_files[0]}'
    
    simulation = args.simulation

    mesh = trimesh.load(mesh_path, force='mesh')
    scale_factor = 1.3  # Scale up by 30%
    mesh.apply_scale(scale_factor)

    output_dir = f'{code_dir}/{args.output_dir}/{args.test_scene_dir}'
    frame_output = args.frame_output
    os.system(f'rm -rf {output_dir}/* && mkdir -p {output_dir}/track_vis {output_dir}/poses')

    to_origin, extents = trimesh.bounds.oriented_bounds(mesh)
    bbox = np.stack([-extents/2, extents/2], axis=0).reshape(2,3)

    scorer = ScorePredictor()
    refiner = PoseRefinePredictor()
    glctx = dr.RasterizeCudaContext()
    est = FoundationPose(model_pts=mesh.vertices, model_normals=mesh.vertex_normals, mesh=mesh, scorer=scorer, refiner=refiner, debug_dir=output_dir, debug=True, glctx=glctx)
    logging.info("Estimator initialization done")

    reader = DTwinReader(video_dir=scene_dir, shorter_side=None, zfar=np.inf)   
    
    while not reader.get_video_detected():
        reader.get_first_frame()
    
    if not simulation:
        create_mask(args.test_scene_dir)
    
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
        
        os.makedirs(f'{output_dir}/poses', exist_ok=True)
        
        # np.save(f'{output_dir}/poses/frame{reader.get_count():06}.npy', pose.reshape(4,4))
        pose.astype('float32').tofile(f'{output_dir}/poses/frame{reader.get_count():06}.bin')
        pose_array.append(pose)
        
        center_pose = pose@np.linalg.inv(to_origin)
        vis = draw_posed_3d_box(reader.K, img=color, ob_in_cam=center_pose, bbox=bbox)
        vis = draw_xyz_axis(color, ob_in_cam=center_pose, scale=0.1, K=reader.K, thickness=3, transparency=0, is_input_rgb=True)
        
        elapsed_time = time.time() - start_time
        time_array.append(elapsed_time)

        if (frame_output):
            os.makedirs(f'{output_dir}/track_vis', exist_ok=True)
            imageio.imwrite(f'{output_dir}/track_vis/frame{reader.get_count():06}.png', vis)
        
        reader.increment_count()
        
        if not reader.get_next_frame_exists():
            break
    
    f = open(f'{output_dir}/timing.txt', "w")
    for i in time_array:
        f.write(f"{i}\n")
    f.close()

    # ----------------------------
    # FOR DATA VALIDATION PURPOSES
    # ----------------------------
    # f = open(f'{output_dir}/poses.txt', "w")
    # frames30 = [0, 250, 475, 590, 700, 825, 1139]
    # frames20 = [0, 166, 316, 394, 466, 550, 761]
    # frames10 = [0, 83, 158, 197, 233, 275, 380]
     
    # with open(f'{output_dir}/poses.txt', 'w') as f:
    #     for i, pose in enumerate(pose_array):
    #         # Write the matrix
    #         logging.info(f'i:{i}')
    #         if i in frames30:
    #             np.savetxt(f, pose, fmt='%g')  # %g uses general format for numbers
            
    #             # Add a line break after each matrix except the last one
    #             if i < len(pose_array) - 1:
    #                 f.write('\n\n')
            
    

    