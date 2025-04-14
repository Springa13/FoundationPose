import os
import time

timing_array = []
f = open(f'debug/timing.txt', "r")
for i in f:
    line = f.readline().rstrip()
    timing_array.append(int(line))
    
f.close()
print(timing_array)

count = 0

while True:
    old_path = f'debug/ob_in_cam/frame{count:06}.npy'
    if not os.path.exists(old_path):
        break

    new_path = f'debug/ob_in_cam/fake{count:06}.npy'
    os.rename(old_path, new_path)

while True:
    old_path = f'debug/ob_in_cam/fake{count:06}.npy'
    if not os.path.exists(old_path):
        break
    time.sleep(timing_array[count])

    new_path = f'debug/ob_in_cam/frame{count:06}.npy'
    os.rename(old_path, new_path)