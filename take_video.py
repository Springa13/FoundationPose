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

fps = sys.argv[2]
res = sys.argv[3]
x_res, y_res = 0
if (res == '144p'):
    x_res, y_res = 256, 144
elif (res == '240p'):
    x_res, y_res = 320, 240
elif (res == '360p'):
    x_res, y_res = 640, 360
elif (res == '480p'):
    x_res, y_res = 854, 480
elif (res == '720p'):
    x_res, y_res = 1280, 720


config.enable_stream(rs.stream.depth, x_res, y_res, rs.format.z16, fps)
config.enable_stream(rs.stream.color, x_res, y_res, rs.format.bgr8, fps)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)
count = 0

dir_path = f'data/{sys.argv[1]}'

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
