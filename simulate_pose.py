import time
import sys
import os
import glob

def rename_simulation_bins(scene_dir):
    print("Preparing poses...")
    dir_path = f'output/{scene_dir}/poses'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, dir_path)

    png_files = sorted(glob.glob(os.path.join(data_dir, '*.bin')))
    
    for i, old_path in enumerate(png_files):
        new_name = f'sim{i:06}.bin'
        new_path = os.path.join(data_dir, new_name)
        if (old_path != new_path):
            os.rename(old_path, new_path)

def simulate_bin_output(scene_dir):
    print("Running pose simulation...")
    timing_array = []

    with open(f'output/{scene_dir}/timing.txt', "r", newline="") as file:  # Handles all line endings
        for line in file:
            timing_array.append(float(line))

    dir_path = f'output/{scene_dir}/poses'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, dir_path)

    bin_files = sorted(glob.glob(os.path.join(data_dir, '*.bin')))

    for i, old_path in enumerate(bin_files):
        # time.sleep(timing_array[i])
        new_name = f'frame{i:06}.bin'
        new_path = os.path.join(data_dir, new_name)
        os.rename(old_path, new_path)

