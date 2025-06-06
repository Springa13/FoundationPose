## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##              Align Depth to Color               ##
#####################################################

# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
import os
import shutil
import sys
import time

if len(sys.argv) != 2:
    print("Incorrect number of arguments:")
    print("'python take_video.py [output_dir]'")
    exit(1)
# Create a pipeline
pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)


config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

depth_stream_profile = profile.get_stream(rs.stream.depth).as_video_stream_profile()
intrinsics = depth_stream_profile.get_intrinsics()

fx = intrinsics.fx
fy = intrinsics.fy
cx = intrinsics.ppx
cy = intrinsics.ppy

# Create the intrinsic matrix
K = np.array([
    [fx,  0, cx],
    [ 0, fy, cy],
    [ 0,  0,  1]
])

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)
count = 0

dir_path = f'data/{sys.argv[1]}'

# Save to a text file
np.savetxt(f"{dir_path}/cam_K.txt", K, fmt="%.6f", delimiter=' ')

try:
    os.mkdir(dir_path)
except OSError as error:
    shutil.rmtree(dir_path) 
    os.mkdir(dir_path)

os.mkdir(f'{dir_path}/rgb')
os.mkdir(f'{dir_path}/depth')

# Streaming loop
try:
    while True:
        time.sleep(5)
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Render images:
        #   depth align to color on left
        #   depth on right
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        #images = np.hstack((bg_removed, depth_colormap))
        img = np.concatenate((color_image, depth_colormap), axis=1)
        cv2.namedWindow('Depth camera RGB Feed', cv2.WINDOW_NORMAL)
        cv2.imshow('Depth camera RGB Feed', img)
        
        key = cv2.waitKey(1)
        #print(color_image.dtype)
        cv2.imwrite(f'{dir_path}/rgb/frame' + f"{count:06}" + ".png", color_image)
        cv2.imwrite(f'{dir_path}/depth/frame' + f"{count:06}" + ".png", depth_image)
        count += 1
        
        
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
