import os

def rename_files(folder_path):
    files = sorted(f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
    count = 0
    for index, old_name in enumerate(files, start=1):
        if old_name == "frame000000.png":
            break
        old_path = os.path.join(folder_path, old_name)
        
        
        # Generate new filename with padded numbers (e.g., frame000001)
        new_name = f'frame{count:06}.png'
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")
        count += 1


# Example Usage
folder_path = "data/mustard/rgb" 
folder_path2 = "data/mustard/depth" # Change this to your actual folder path
folder_path3 = "data/mustard/masks"
rename_files(folder_path)
rename_files(folder_path2)
rename_files(folder_path3)
