import subprocess 


# make video through FFMPEG.
def process_video(path,frameRate):
    # -y for output file overwrite
    # -r for frame rate
    # -i for input files
    # -vf for adding subtitles for output video
    cmd = "ffmpeg -y" + " -r " +  str(frameRate) +  " -i " + path + "/%05d.jpg " + " -vf subtitles=output.srt " + " " + path+ "OutputVideo.mkv"
    subprocess.call(cmd, shell=True)
    return print("video is created")
