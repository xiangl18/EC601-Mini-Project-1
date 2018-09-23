import video
import get
import label_process

path = input('Please inpute path：') # path = 'G:/Images/'
frame_rate = input('Please inpute frame_rate：')

# get.twitter_images(path)
get.search_images(path)
get.image_process(path, 900, 600)
label_process.srt(path, frame_rate)
video.process_video(path, frame_rate)







