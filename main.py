import os 
import video
import get
import label_process

while True:
  path = input('Please input path(Please add "\" at the end of your path):')
  # Provide a default
    if not path:
      default = os.getcwd()
      path = default + "/images/"
      if (not os.path.exists(path)):
        os.mkdir(path)
  # Check whether the file is writable
  if not os.access(path, os.W_OK):
    print("Path not writable, please try again")
  else:
    break

while True:
  frame_rate = input('Please inpute frame rate (Frame rate should be input by decimals):')
  try:
      float(frame_rate)
      break
  except ValueError:
      print("Frame rate not a number, please try again")

# you can get user's own homeline by using line 26 as:  
get.twitter_images(path)
#you can also search images from users' homeline by using line 28 as: 
#get.search_images(path)
               
#It is better to resize images into smaller size if there are lots of images needed to be transformed.              
get.image_process(path, 900, 600)
label_process.srt(path, frame_rate)
video.process_video(path, frame_rate)
