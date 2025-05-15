import socket
import time
import numpy as np

ROBOT_IP = '192.168.125.1'  # Change this to your robot IP
ROBOT_PORT = 1025           # Change this to your configured socket port

# Example targets: [x, y, z, q1, q2, q3, q4]
targets = [
    [500, 0, 400, 1, 0, 0, 0],
    [500, 100, 400, 1, 0, 0, 0],
    [500, 100, 300, 1, 0, 0, 0],
    [500, 0, 300, 1, 0, 0, 0],
    [500, 0, 400, 1, 0, 0, 0],
]

received_poses = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to ABB robot...")
    s.connect((ROBOT_IP, ROBOT_PORT))
    s.settimeout(2)

    for target in targets:
        # Convert to space-separated string
        target_str = ' '.join(map(str, target)) + '\n'
        s.sendall(target_str.encode())

        # Receive pose at 15 Hz
        try:
            data = s.recv(1024)
            if data:
                pose_str = data.decode().strip()
                numbers = list(map(float, pose_str.split()))
                if len(numbers) == 16:
                    matrix = np.array(numbers).reshape((4, 4))
                    received_poses.append(matrix)
                    print("Got pose:\n", matrix)
        except socket.timeout:
            print("No pose received (timeout).")

        time.sleep(1 / 15)

print(f"\nTotal poses received: {len(received_poses)}")
