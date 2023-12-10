#


import os
import moviepy.video.io.ImageSequenceClip
image_folder='data'
output_path='my_video2.mp4'

fps=24

image_files = [os.path.join(image_folder,img)
               for img in os.listdir(image_folder)
               if img.endswith(".jpg")]

image_files = sorted(image_files)

clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)

clip.write_videofile(output_path)
