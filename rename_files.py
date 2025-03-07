import os

def rename_files(folder_path, simulate):
    if simulate:
        prefix = 'fake'
    else:
        prefix = 'frame'

    files = sorted(f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
    count = 0
    for index, old_name in enumerate(files, start=1):
        if old_name == f'{prefix}000000.png':
            break
        
        old_path = os.path.join(folder_path, old_name)
        
        # Generate new filename with padded numbers (e.g., frame000001)
        new_name = f'{prefix}{count:06}.png'
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")
        count += 1


