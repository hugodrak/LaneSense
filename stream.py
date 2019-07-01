from moviepy.editor import VideoFileClip
from pipeline import pipeline
import os, sys

out_file = 'test_with_lines.mp4'
# # change fps_source if file is string [fps, tbr]
in_file = sys.argv[1]
mode = int(sys.argv[2])
# out_file = sys.argv[3]

if mode == 1:
    source = VideoFileClip(in_file, fps_source="fps")
    white_clip = source.fl_image(pipeline)
    white_clip.write_videofile(out_file, audio=False, fps=30.3)
elif mode == 2:
    source = VideoFileClip(in_file, fps_source="fps")
    img = source.fl_image(pipeline)
    
