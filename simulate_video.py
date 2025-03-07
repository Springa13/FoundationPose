import time
import sys
import os

# Define the frame rate (24fps)
fps = 15
frame_time = 1 / fps  # Time for each frame (in seconds)

dir_path = f'data/{sys.argv[1]}'
count = 0

while True:
    # Record the time at the start of the frame
    start_time = time.time()

    # Your frame processing code goes here
    # For example, print something to simulate frame processing
    os.rename(f'{dir_path}/rgb/frame{count:06}.png')
    count += 1

    # Calculate how much time has passed and sleep to maintain the frame rate
    elapsed_time = time.time() - start_time
    sleep_time = frame_time - elapsed_time

    # If we have extra time before the next frame, sleep
    if sleep_time > 0:
        time.sleep(sleep_time)
