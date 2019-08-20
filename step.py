import cv2, sys, os, argparse, time
from moviepy.editor import VideoFileClip
import matplotlib.pyplot as plt
import numpy as np

from lines import get_lines
from plates import get_plates
from signs import get_signs

parser = argparse.ArgumentParser(description='Detect objects around the road.')
parser.add_argument('-f', '--file', help='The videofile to step through')
parser.add_argument('-r', '--rate', help='rate rate through file ex. 200ms', type=int)
parser.add_argument('-s', '--start', help='where in the video sequence to start ex 2s', type=int)
parser.add_argument('-v', '--views', help='which views to show ex. 1,2,3')


args = parser.parse_args()

## standard command  python step.py --file logs/chl101_op/test5.mp4 --rate 400 --start 10 -v 1,2,3


class Plot:
    input_img = np.zeros((500,800,3), np.uint8)
    processed_images = []
    width = 355
    height = 200
    windows = 0
    views = {"lines": False, "signs": False, "plates": False}

    def __init__(self):
        views = args.views.split(',')

        if "1" in views:
            self.views["lines"] = True
            self.windows += 1
        if "2" in views:
            self.views["signs"] = True
            self.windows += 1
        if "3" in views:
            self.views["plates"] = True
            self.windows += 1



    def draw(self, images):
        for image in images:
            resized = cv2.resize(image[1], (self.width, self.height))
            cv2.imshow(image[0], resized)


    def update(self, image):
        self.input_img = image.copy()

        if self.views['lines']:
            self.processed_images.append(("Lines", get_lines(self.input_img)))

        if self.views['signs']:
            self.processed_images.append(("Signs", get_signs(self.input_img)))

        if self.views['plates']:
            self.processed_images.append(("Plates", get_plates(self.input_img)))

        #
        # self.images = [("Lines", get_lines(self.input_img)), ("Signs", get_signs(self.input_img)), ("Plates", get_plates(self.input_img))]
        # self.images = [get_lines(self.input_img), get_plates(self.input_img), get_signs(self.input_img)]
        self.draw(self.processed_images)

    def shape(self, widht, height):
        self.width = width
        self.height = height

    def images(self, images):
        self.images = images

    def auto_fit(self, screen_width):
        if self.windows == 1:
            self.width = 1000
            self.height = 500
        else:
            self.width = int(screen_width/self.windows)
            self.height = int(self.width/1.777)

        i = 0
        images = self.processed_images

        for image in images:
            cv2.moveWindow(image[0], self.width*i, 0 )
            i+=1

in_file = args.file
print(in_file)
source = VideoFileClip(in_file, fps_source="fps")
duration = source.duration
print("Duration: " + str(duration))
time_frame = float(args.rate)/1000
# time_frame = float(float(int(args.rate)/1000)
# print(time_frame)

time_clip = float(args.start)
show = True

def toggle_images(key):
    global time_clip, show
    # print(time_clip)
    if key == 83:
        time_clip += time_frame
    elif key == 81:
        time_clip -= time_frame

    if (time_clip >= (duration-time_frame)):
        time_clip = 0
        print("Reached end of file!")
    if key == 116:
        print(time_clip)
    if key == 113:
        show = False
        return

    sys.stdout.flush()

main_plot = Plot()
main_plot.update(source.get_frame(time_clip))
main_plot.auto_fit(1366)

while show:
    key = cv2.waitKey(50)

    if not key == -1:
        toggle_images(key)
        # print(time_clip)
        main_plot.update(source.get_frame(time_clip))
