from pipeline import pipeline
from moviepy.editor import VideoFileClip

import cv2, sys, os
import matplotlib.pyplot as plt
import numpy as np

in_file = sys.argv[1]
source = VideoFileClip(in_file, fps_source="fps")
duration = source.duration
print("Duration: " + str(duration))
time_frame = float(float(sys.argv[2])/1000)
print(time_frame)
plt.figure()
time = 0
show = True
line_image = pipeline(source.get_frame(time))

def toggle_images(event):
    global time
    sys.stdout.flush()
    key = event.key
    if key == "right":
        time += time_frame
    elif key == "left":
        time -= time_frame

    if (time >= duration):
        time = 0
        print("Reached end of file!")

    print(time)
    line_image = pipeline(source.get_frame(time))
    global fig
    fig.set_data(line_image)
    plt.show()
#----------------------------------

plt.connect('key_press_event', toggle_images)
fig = plt.imshow(line_image)

plt.show()
