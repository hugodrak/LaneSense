from lines import get_lines
from plates import get_plates
from signs import get_signs

from moviepy.editor import VideoFileClip

import cv2, sys, os
import matplotlib.pyplot as plt
import numpy as np
import time

in_file = sys.argv[1]
source = VideoFileClip(in_file, fps_source="fps")
duration = source.duration
print("Duration: " + str(duration))
time_frame = float(float(sys.argv[2])/1000)
print(time_frame)
fig, (ax1, ax2, ax3) = plt.subplots(1,3)

# fig, (ax1, ax2) = plt.subplots(1,2)

time = int(sys.argv[3])
show = True
# line_image, cropped_image, mask_image = pipeline(source.get_frame(time))

def toggle_images(event):
    global time
    sys.stdout.flush()
    key = event.key

    if key == "right":
        time += time_frame
    elif key == "left":
        time -= time_frame

    if (time >= (duration-time_frame)):
        time = 0
        print("Reached end of file!")
    if key == "q":
        return

    print(time)

    frame = source.get_frame(time)
    line_image, cropped_image, mask_image = pipeline()

while show:
    if cv2.waitKey(33) == ord('a'):
        print "pressed a"
    time.sleep(1)
