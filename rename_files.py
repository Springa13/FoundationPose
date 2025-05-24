import os
import sys

def rename_files(folder):
    rgb_path = f'data/{folder}/rgb'
    depth_path = f'data/{folder}/depth'
    mask_path = f'data/{folder}/mask'

    rgb_files = sorted(f for f in os.listdir(rgb_path) if os.path.isfile(os.path.join(rgb_path, f)))
    depth_files = sorted(f for f in os.listdir(depth_path) if os.path.isfile(os.path.join(depth_path, f)))
    mask_files = sorted(f for f in os.listdir(mask_path) if os.path.isfile(os.path.join(mask_path, f)))
    
    count = 0
    for index, old_name in enumerate(rgb_files, start=1):
        
        old_path = os.path.join(rgb_path, old_name)
        
        # Generate new filename with padded numbers (e.g., frame000001)
        new_name = f'frame{count:06}.png'
        new_path = os.path.join(rgb_path, new_name)

        os.rename(old_path, new_path)
        count += 1
    
    count = 0
    for index, old_name in enumerate(depth_files, start=1):
        
        old_path = os.path.join(depth_path, old_name)
        
        # Generate new filename with padded numbers (e.g., frame000001)
        new_name = f'frame{count:06}.png'
        new_path = os.path.join(depth_path, new_name)

        os.rename(old_path, new_path)
        count += 1

    count = 0
    for index, old_name in enumerate(mask_files, start=1):
        
        old_path = os.path.join(mask_path, old_name)
        
        # Generate new filename with padded numbers (e.g., frame000001)
        new_name = f'frame{count:06}.png'
        new_path = os.path.join(mask_path, new_name)

        os.rename(old_path, new_path)
        count += 1


