import time
import sys
import os
import glob

def rename_simulation_images(scene_dir):

    dir_path = f'data/{scene_dir}/rgb'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, dir_path)

    png_files = sorted(glob.glob(os.path.join(data_dir, '*.png')))

    for i, old_path in enumerate(png_files):
        new_name = f'sim{i:06}.png'
        new_path = os.path.join(data_dir, new_name)
        os.rename(old_path, new_path)

def simulate_video_input(scene_dir, fps):

    # Define the frame rate (24fps)
    frame_time = 1 / fps  # Time for each frame (in seconds)
    
    dir_path = f'data/{scene_dir}/rgb'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, dir_path)

    png_files = sorted(glob.glob(os.path.join(data_dir, '*.png')))

    for i, old_path in enumerate(png_files):
        start_time = time.time()
        new_name = f'frame{i:06}.png'
        new_path = os.path.join(data_dir, new_name)
        os.rename(old_path, new_path)
        # Calculate how much time has passed and sleep to maintain the frame rate
        elapsed_time = time.time() - start_time
        sleep_time = frame_time - elapsed_time

        # If we have extra time before the next frame, sleep
        if sleep_time > 0:
            time.sleep(sleep_time)


scene_dir = sys.argv[1]
fps = sys.argv[2]
simulate_video_input(scene_dir, fps)
