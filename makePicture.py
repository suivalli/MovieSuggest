import cv2
import numpy as np
import sys
from pprint import pprint

PICTURE_WIDTH = 3840
PICTURE_HEIGHT = 2160

VERBOSE = False

def cli_progress(current_val, end_val, bar_length=20):
    percent = float(current_val) / end_val
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()

def getDominant(img):
    Z = img.reshape((-1,3))
    Z = np.float32(Z)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 3

    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]

    return res[0]

def makePicture(videofile, outputname):
    pic = np.zeros((PICTURE_HEIGHT,PICTURE_WIDTH,3), np.uint8)
    values = []
    c = cv2.VideoCapture(videofile)
    print c.isOpened()

    framecount = c.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(c.get(cv2.CAP_PROP_FPS))

    if VERBOSE:
        print "Frame count: " + str(framecount)
        print "FPS: " + str(fps)

    frames = 1
    while frames < framecount:
        if frames % fps == 0:
            ret, img = c.read()
            values.append(getDominant(img))
            if VERBOSE:
                cli_progress(frames,framecount)
                print ("\t" + str(frames) + "/" + str(int(framecount)) + " completed")
        frames += 1
    '''
    width_array = []
    values_index = 0
    block_width = PICTURE_WIDTH / len(values)
    i = 1
    while i <= PICTURE_WIDTH:
        width_array.append(values[values_index])
        if block_width % i == 0:
            values_index += 1
            print "Value " + str(values_index) + " out of " + str(len(values))
        i += 1

    for i in range(0,PICTURE_HEIGHT):
        pic[i] = width_array
    '''

    pic = np.zeros((PICTURE_HEIGHT, len(values), 3), np.uint8)

    for i in range(0,PICTURE_HEIGHT):
        pic[i] = values


    res = cv2.resize(pic,(PICTURE_WIDTH, PICTURE_HEIGHT), interpolation= cv2.INTER_CUBIC)
    cv2.imwrite("starwarsOrig.jpg", pic)
    cv2.imwrite(outputname,res)



VERBOSE = True


makePicture('starwars1.mp4', 'starwars.jpg')