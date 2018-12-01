import re
import os
import googleVision

# make srt file from labels.
def srt(path, framerate):
    n = 0
    T = 0
    filelist = os.listdir(path)
    timeline = ['00', '00', '00']
    second = '0'
    srtfile = open('output.srt', 'w')
    # make judgement about how many images in file.
    if len(filelist) == 0:
        raise Exception('None pictures found')
    else:
        if len(filelist) > 100:
            raise Warning('More than 100 pictures')
    frame_rate = float(framerate)
    # make srt
    for file in filelist:
        label = googleVision.label(path + file)
        for i in range(len(label)):
            labels = ', '.join(label)
        start = ':'.join(timeline) + '.'+second

        T = T + 1./frame_rate
        timeline[2], second = str(T).split('.')
        if int(timeline[2]) == 60:
            timeline[1] = str(int(timeline[1]) + 1)
            timeline[2] = '00'
            T = T - 60
        end = ':'.join(timeline) + '.'+second
        line = [str(n+1), start + ' --> ' + end, labels]
        line = '\n'.join(line)
        srtfile.write(line + '\n'+'\n')
        n = n + 1
    return print("srt is created")


