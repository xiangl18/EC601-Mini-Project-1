import video
import get
import label_process

path = input('Please inpute path：') 
frame_rate = input('Please inpute frame rate(frame rate should be input by decimals):')

# you can also get user's own homeline by using line 9 as:  
# get.twitter_images(path)
get.search_images(path)
get.image_process(path, 900, 600)
label_process.srt(path, frame_rate)
video.process_video(path, frame_rate)







