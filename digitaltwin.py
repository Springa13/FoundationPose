import subprocess
from pathlib import Path

# Get path to the .exe
exe_path = Path(__file__).parent / "digitaltwin" / "game.exe"

# Set the working directory to where the .exe is located
subprocess.run([str(exe_path)], cwd=exe_path.parent)