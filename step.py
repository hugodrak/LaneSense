from lines import get_lines
from plates import get_plates
from signs import get_signs

from moviepy.editor import VideoFileClip

import cv2, sys, os
import matplotlib.pyplot as plt
import numpy as np
import time

class Plot:
    input_img = np.zeros((500,800,3), np.uint8)
    images = []
    width = 355
    height = 200
    windows = 3

    def draw(self, images):
        for image in images:
            resized = cv2.resize(image[1], (self.width, self.height))
            cv2.imshow(image[0], resized)

    def update(self, image):
        self.input_img = image.copy()
        self.images = [("Lines", get_lines(self.input_img)), ("Signs", get_signs(self.input_img)), ("Plates", get_plates(self.input_img))]
        # self.images = [get_lines(self.input_img), get_plates(self.input_img), get_signs(self.input_img)]
        self.draw(self.images)

    def shape(self, widht, height):
        self.width = width
        self.height = height

    def images(self, images):
        self.images = images

    def auto_fit(self, screen_width):
        self.width = int(screen_width/self.windows)
        self.height = int(self.width/1.777)


in_file = sys.argv[1]
source = VideoFileClip(in_file, fps_source="fps")
duration = source.duration
print("Duration: " + str(duration))
time_frame = float(float(sys.argv[2])/1000)
print(time_frame)
# fig, (ax1, ax2, ax3) = plt.subplots(1,3)
#
# # fig, (ax1, ax2) = plt.subplots(1,2)
#
time_clip = int(sys.argv[3])
show = True
# # line_image, cropped_image, mask_image = pipeline(source.get_frame(time_clip))
#
def toggle_images(key):
    global time_clip, show
    print(time_clip)
    if key == 83:
        time_clip += time_frame
    elif key == 81:
        time_clip -= time_frame

    if (time_clip >= (duration-time_frame)):
        time_clip = 0
        print("Reached end of file!")

    if key == 113:
        show = False
        return

    sys.stdout.flush()


#     print(time_clip)
    #cv2.circle(img,(447,63), 63, (0,0,255), -1)
#
#
#     line_image, cropped_image, mask_image = pipeline(
# img = np.zeros((500,800,3), np.uint8)
# cv2.circle(img,(447,63), 63, (0,0,255), -1)
# cv2.imshow("temp", img)

main_plot = Plot()
main_plot.auto_fit(1366)
main_plot.update(source.get_frame(time_clip))

while show:
    key = cv2.waitKey(100)

    if not key == -1:
        toggle_images(key)
        print(time_clip)
        main_plot.update(source.get_frame(time_clip))
