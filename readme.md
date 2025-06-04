# Real-Time Pose Estimation with FoundationPose: Exploring the Possibility of Using a 6D Pose Estimation Model for Digital Twin Technologies

This is a fork of the implementation found [[here]](https://github.com/NVlabs/FoundationPose) and described below:

We present FoundationPose, a unified foundation model for 6D object pose estimation and tracking, supporting both model-based and model-free setups. Our approach can be instantly applied at test-time to a novel object without fine-tuning, as long as its CAD model is given, or a small number of reference images are captured. We bridge the gap between these two setups with a neural implicit representation that allows for effective novel view synthesis, keeping the downstream pose estimation modules invariant under the same unified framework. Strong generalizability is achieved via large-scale synthetic training, aided by a large language model (LLM), a novel transformer-based architecture, and contrastive learning formulation. Extensive evaluation on multiple public datasets involving challenging scenarios and objects indicate our unified approach outperforms existing methods specialized for each task by a large margin. In addition, it even achieves comparable results to instance-level methods despite the reduced assumptions.

# Changes

Writing...

# Data

The FoundationPose model network weights and SAM model weights can be downloaded from [here](https://drive.google.com/file/d/1kGb9EXD8YcYmm5H6zyQDWW6PYr7mVf0Q/view?usp=sharing). The weights folder can be downloaded, unzipped and placed in the FoundationPose directory as is. 

Also provided is the experimental [input](https://drive.google.com/file/d/1PEVdxEOqJyZ78C9Q7-jkRx8N8mrTY_fg/view?usp=sharing) (5.23GB) and [output](https://drive.google.com/file/d/1j8990gk_XpuDEu6S81fN887od2oKD45Y/view?usp=sharing) (3.91GB) data as part of the MXEN4004 Mechatronics Research Project. The input and output data contain nine datasets (eg. 720_10) that must be put into the 'data' directory.

Finally, the validation dataset as originally provided by the NVLabs/FoundationPose Github repository can be downloaded [here](https://drive.google.com/drive/folders/1pRyFmxYXmAnpku7nGRioZaKrVJtIsroP?usp=sharing).

In my research project i also run the FoundationPose model on this validation dataset and the results of that is shown [here]()


# Setup Option 1: Docker
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


# Setup Option 2: Conda

- To set up using conda, run the install_dependencies.sh file. This file assumes conda has been installed on the system, but can be changed by uncommenting out lines 7-10.


# Run program

The program can be run through the main.py file for running all the video acquistion system, foundationpose model, and digital twin through. It has a command line interface that is easy to follow along with (i think) to be able to select what to run and when to run them. The main.py program may be slightly buggy or not work with some other programs.

Alternatively, each part of the program can be run individually as detailed below:
1. Video Acquisiton System

Run through the 'take_video.py' file.
'''
python take_video.py [resolution] [fps]
'''

2. FoundationPose Model
  The paths have been set in argparse by default. If you need to change the scene, you can pass the args accordingly. By running on the validation data, you should be able to see the robot manipulating the mustard bottle. Pose estimation is conducted on the first frame, then it automatically switches to tracking mode for the rest of the video. The resulting visualizations will be saved to the `output/{data_folder}` specified in the argparse.
  ```
  python run_pose.py
  ```
  For running the experimental scene inputs or custom inputs, simply place the data folder (eg. 360_10) into the data folder and run the following:
  ```
  python run_pose.py --test_scene_dir 360_10
  ```


3. Digital Twin
Run through the file located at 'digitaltwin/FPDT.exe'.
If it doesn't work on your system the file 'main.cpp' in the same directory must be recompiled.
After compiling the executable can be run from within the digitaltwin directory as shown below:
```
./FPDT.exe [data_folder]
```
For this to work, both the input folder and the output folder of the 'data_folder' name must be present
'''

# License
The code and data are released under the NVIDIA Source Code License. Copyright © 2024, NVIDIA Corporation. All rights reserved.
