import video
import get
import label_process

while True:
  path = input('Please input path:')
  # Provide a default
  if not path:
    path = "./"
  # Check whether the file is writable
  if not os.access(path, os.W_OK):
    print("Path not writable, please try again")
  else:
    break

while True:
  frame_rate = input('Please inpute frame rate (frame rate should be input by decimals):')
  try:
      float(frame_rate)
      break
  except ValueError:
      print("Frame rate not a number, please try again")

# you can also get user's own homeline by using line 9 as:  
# get.twitter_images(path)
get.search_images(path)
get.image_process(path, 900, 600)
label_process.srt(path, frame_rate)
video.process_video(path, frame_rate)
