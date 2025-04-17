import subprocess
from pathlib import Path
import os

def run_digital_twin(data_folder):
    print("Running digital twin program...")
    exe_path = Path(__file__).parent / "digitaltwin" / "FPDT.exe"
    dt_process = subprocess.Popen([str(exe_path), data_folder], cwd=exe_path.parent, stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)
    return dt_process

def run_foundation_pose(data_folder):
    print("Running FoundationPose...")
    fp_process = subprocess.Popen(["python", "run_pose_mod.py", data_folder])
    return fp_process

def run_video():
    print("Taking video...")
    v_process = subprocess.Popen(["python", "take_video.py"])
    return v_process

default_launch = input("Use default launch sequence (y/n): ")

while default_launch != 'y' and default_launch != 'n':
    default_launch = input("Use default launch sequence (y/n): ")

data_folder = input("Enter data folder name: ")

if default_launch == 'y':
    
    run_digital_twin(data_folder)
    run_foundation_pose(data_folder)
    run_video()
else:
    dt_running = False
    fp_running = False
    v_running = False
    dt_process = None
    while True:
        print("--------------------------------")
        print("Select program to run/terminate:\n\n\t1. digital twin\n\t2. pose estimation\n\t3. video\n\tx. exit")
        print("--------------------------------")
        selection = input("Select: ")

        while selection != '1' and selection != '2' and selection != '3' and selection != 'x':
            selection = input("Select: ")
        
        if selection == '1':
            if dt_process is None or dt_process.poll() is not None:
                dt_process = run_digital_twin(data_folder)
            else:
                dt_process.terminate()

        elif selection == '2':
            if fp_process is None or fp_process.poll() is not None:
                fp_process = run_foundation_pose(data_folder)
            else:
                fp_process.terminate()
            
        elif selection == '3':
            if (v_running):
                v_process.terminate()
                fp_running = False
            else:
                v_process = run_video()
                v_running = True
            
        elif selection == 'x':
            break
