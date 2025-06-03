import subprocess
from pathlib import Path
import os
import glob
import time

def run_digital_twin(data_folder):
    print("Running digital twin program...")
    exe_path = Path(__file__).parent / "digitaltwin" / "FPDT.exe"
    dt_process = subprocess.Popen([str(exe_path), data_folder], cwd=exe_path.parent, stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)
    return dt_process

def run_foundation_pose(data_folder, simulate):
    print("Running FoundationPose...")
    fp_process = subprocess.Popen(["python", "run_pose_mod.py", '--test_scene_dir', data_folder, '--simulate', simulate])
    return fp_process

def run_video(data_folder):
    fps = int(input('Target FPS: '))
    res = input('Target Resolution (144p, 240p, 360p, 480p, 720p): ')
    print("Taking video...")
    v_process = subprocess.Popen(["python", "take_video.py", data_folder, fps, res])
    return v_process

def run_simulate_video(data_folder):
    fps = int(input('Target FPS: '))
    print("Running video simulation...")
    sv_process = subprocess.Popen(["python", "simulate_video.py", data_folder, fps])
    return sv_process

    

default_launch = input("Use default launch sequence (y/n): ")

while default_launch != 'y' and default_launch != 'n':
    default_launch = input("Use default launch sequence (y/n): ")

data_folder = input("Enter data folder name: ")

if default_launch == 'y':
    
    run_digital_twin(data_folder)
    run_foundation_pose(data_folder)
    run_video()
else:
    
    dt_process = None
    fp_process = None
    v_process = None
    sv_process = None
    while True:
        print("--------------------------------")
        print("Select program to run/terminate:\n\n\t1. digital twin\n\t2. pose estimation\n\t3. video\n\t4. simulate video\n\t5. simulate pose\n\tx. exit")
        print("--------------------------------")
        selection = input("Select: ")

        while selection not in ['1', '2', '3', '4', '5', 'x']:
            selection = input("Select: ")
        
        if selection == '1':
            if dt_process is None or dt_process.poll() is not None:
                dt_process = run_digital_twin(data_folder)
            else:
                dt_process.terminate()

        elif selection == '2':
            if fp_process is None or fp_process.poll() is not None:
                fp_process = run_foundation_pose(data_folder, False)
            else:
                fp_process.terminate()
            
        elif selection == '3':
            if v_process is None or v_process.poll() is not None:
                v_process = run_video(data_folder)
            else:
                v_process.terminate()
            
        elif selection == '4':
            if sv_process is None or sv_process.poll() is not None:
                sv_process = run_simulate_video(data_folder, True)
            else:
                sv_process.terminate()
            
            
            
        elif selection == 'x':
            break
