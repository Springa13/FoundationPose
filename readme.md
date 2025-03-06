# Real-Time Pose Estimation with FoundationPose: Exploring the Possibility of 

This is a fork of the implementation found [[here]](https://github.com/NVlabs/FoundationPose) and described below:

We present FoundationPose, a unified foundation model for 6D object pose estimation and tracking, supporting both model-based and model-free setups. Our approach can be instantly applied at test-time to a novel object without fine-tuning, as long as its CAD model is given, or a small number of reference images are captured. We bridge the gap between these two setups with a neural implicit representation that allows for effective novel view synthesis, keeping the downstream pose estimation modules invariant under the same unified framework. Strong generalizability is achieved via large-scale synthetic training, aided by a large language model (LLM), a novel transformer-based architecture, and contrastive learning formulation. Extensive evaluation on multiple public datasets involving challenging scenarios and objects indicate our unified approach outperforms existing methods specialized for each task by a large margin. In addition, it even achieves comparable results to instance-level methods despite the reduced assumptions.

# Data prepare


1) Download all network weights from [here](https://drive.google.com/drive/folders/1DFezOAD0oD1BblsXVxqDsl8fj0qzB82i?usp=sharing) and put them under the folder `weights/`. For the refiner, you will need `2023-10-28-18-33-37`. For scorer, you will need `2024-01-11-20-02-45`.

1) [Download demo data](https://drive.google.com/drive/folders/1pRyFmxYXmAnpku7nGRioZaKrVJtIsroP?usp=sharing) and extract them under the folder `demo_data/`


# Env setup option 1: docker (recommended)
  ```
  cd docker/
  docker pull wenbowen123/foundationpose && docker tag wenbowen123/foundationpose foundationpose  # Or to build from scratch: docker build --network host -t foundationpose .
  bash docker/run_container.sh
  ```

If it's the first time you launch the container, you need to build extensions. Run this command *inside* the Docker container.
```
bash build_all.sh
```

Later you can execute into the container without re-build.
```
docker exec -it foundationpose bash
```

For more recent GPU such as 4090, refer to [this](https://github.com/NVlabs/FoundationPose/issues/27).
In short, do the following:
```
docker pull shingarey/foundationpose_custom_cuda121:latest
```
Then modify the bash script to use this image instead of `foundationpose:latest`.


# Env setup option 2: conda (experimental)

- Setup conda environment

```bash
# create conda environment
conda create -n foundationpose python=3.9

# activate conda environment
conda activate foundationpose

# Install Eigen3 3.4.0 under conda environment
conda install conda-forge::eigen=3.4.0
export CMAKE_PREFIX_PATH="$CMAKE_PREFIX_PATH:/eigen/path/under/conda"

# install dependencies
python -m pip install -r requirements.txt

# Install NVDiffRast
python -m pip install --quiet --no-cache-dir git+https://github.com/NVlabs/nvdiffrast.git

# Kaolin (Optional, needed if running model-free setup)
python -m pip install --quiet --no-cache-dir kaolin==0.15.0 -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.0.0_cu118.html

# PyTorch3D
python -m pip install --quiet --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py39_cu118_pyt200/download.html

# Build extensions
CMAKE_PREFIX_PATH=$CONDA_PREFIX/lib/python3.9/site-packages/pybind11/share/cmake/pybind11 bash build_all_conda.sh
```


# Run model-based demo
The paths have been set in argparse by default. If you need to change the scene, you can pass the args accordingly. By running on the demo data, you should be able to see the robot manipulating the mustard bottle. Pose estimation is conducted on the first frame, then it automatically switches to tracking mode for the rest of the video. The resulting visualizations will be saved to the `debug_dir` specified in the argparse. (Note the first time running could be slower due to online compilation)
```
python run_demo.py
```


# Training data download
Our training data include scenes using 3D assets from GSO and Objaverse, rendered with high quality photo-realism and large domain randomization. Each data point includes **RGB, depth, object pose, camera pose, instance segmentation, 2D bounding box**. [[Google Drive]](https://drive.google.com/drive/folders/1s4pB6p4ApfWMiMjmTXOFco8dHbNXikp-?usp=sharing).

- To parse the camera params including extrinsics and intrinsics
  ```
  with open(f'{base_dir}/camera_params/camera_params_000000.json','r') as ff:
    camera_params = json.load(ff)
  world_in_glcam = np.array(camera_params['cameraViewTransform']).reshape(4,4).T
  cam_in_world = np.linalg.inv(world_in_glcam)@glcam_in_cvcam
  world_in_cam = np.linalg.inv(cam_in_world)
  focal_length = camera_params["cameraFocalLength"]
  horiz_aperture = camera_params["cameraAperture"][0]
  vert_aperture = H / W * horiz_aperture
  focal_y = H * focal_length / vert_aperture
  focal_x = W * focal_length / horiz_aperture
  center_y = H * 0.5
  center_x = W * 0.5

  fx, fy, cx, cy = focal_x, focal_y, center_x, center_y
  K = np.eye(3)
  K[0,0] = fx
  K[1,1] = fy
  K[0,2] = cx
  K[1,2] = cy
  ```


# License
The code and data are released under the NVIDIA Source Code License. Copyright © 2024, NVIDIA Corporation. All rights reserved.
