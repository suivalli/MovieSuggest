import cv2
import numpy as np
import sys
import Image
import getopt
import time
import subprocess
import colorsys
import os

PICTURE_WIDTH = 3840
PICTURE_HEIGHT = 2160

NUM_CLUSTERS = 5
VERBOSE = False

def cli_progress(current_val, end_val, filename, bar_length=20):
    percent = float(current_val) / end_val
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\rPercent: [{0}] {1}%\tfile {2}".format(hashes + spaces, int(round(percent * 100)), filename))
    sys.stdout.flush()
'''
def getDominant(img):
    Z = img.reshape((-1,3))
    Z = np.float32(Z)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 2

    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]

    return res[0]
'''

def makeTestVideo():
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 25.0
    video = cv2.VideoWriter("test.avi",fourcc,fps,(1280,720))
    pic = np.zeros((720, 1280, 3), np.uint8)
    for i in range(0,1000):
        video.write(pic)
        if i == 500:
            pic[pic == 0] = 255

def getColor(img):
    img = Image.fromarray(img)
    img = img.resize((150,150))

    result = img.convert('P', palette=Image.ADAPTIVE, colors = 5)
    result.putalpha(0)
    colors = result.getcolors(150*150)

    maxBrightness = 0
    indexBrightness = 0
    for i in range(0,len(colors)):
        coll = sum(colors[i][1])
        if coll > maxBrightness:
            maxBrightness = coll
            indexBrightness = i

    max = 0
    index = 0
    for i in range(0,len(colors)):
        if colors[i][0] > max:
            max = colors[i][0]
            index = i

    maxColor = (float(colors[index][1][0])/255, float(colors[index][1][1])/255, float(colors[index][1][2])/255)
    maxColor = colorsys.rgb_to_hsv(maxColor[0],maxColor[1],maxColor[2])

    if (maxColor[2]) >= 0.15:
        BGR = list(reversed(colors[index][1][0:3]))
    else:
        BGR = list(reversed(colors[indexBrightness][1][0:3]))
    return BGR

def makePicture(videofile, outputname):
    start_time = int(round(time.time() * 1000))
    values = []
    c = cv2.VideoCapture(videofile)
    if VERBOSE:
        if c.isOpened():
            print ("Video succesfully loaded.")
        else:
            print ("Video not loaded")


    framecount = c.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(c.get(cv2.CAP_PROP_FPS))

    if VERBOSE:
        print "Frame count: " + str(framecount)
        print "FPS: " + str(fps)

    frames = 1
    while frames < framecount:
        if frames % fps != 0:
            ret = c.grab()
        elif frames % fps == 0:
            ret, img = c.read()
            if ret:
                values.append(getColor(img))
            if VERBOSE:
                cli_progress(frames,framecount, outputname)
                #print ("\t" + str(frames) + "/" + str(int(framecount)) + " completed")
        frames += 1

    pic = np.zeros((PICTURE_HEIGHT, len(values), 3), np.uint8)
    for i in range(0,PICTURE_HEIGHT):
        pic[i] = values

    dat = np.zeros((1, len(values), 3), np.uint8)
    dat[0] = values
    dat = cv2.resize(dat,(PICTURE_WIDTH, 1), interpolation=cv2.INTER_CUBIC)
    res = cv2.resize(pic,(PICTURE_WIDTH, PICTURE_HEIGHT), interpolation= cv2.INTER_CUBIC)
    cv2.imwrite("pics/" + outputname + "_dat.jpg", dat)
    cv2.imwrite("pics/" + outputname + "_orig.jpg", pic)
    cv2.imwrite("pics/" + outputname + ".jpg",res)

    end_time = int(round(time.time() * 1000))
    elapsed_time = (end_time - start_time)/1000

    if VERBOSE:
        print ("Finished in " + str(elapsed_time) + " seconds.")

def getAudio(videofile):
    command = "ffmpeg -i " + videofile + " -ab 160k -ac 2 -ar 44100 -vn audio.mp3"

    subprocess.call(command, shell=True)

    if VERBOSE:
        print "Audio made!"

def getMovieFiles(directory):
    filesArray = []
    madeArray = []
    for root, dirs, files in os.walk("pics/"):
        for file in files:
            if file.endswith("_dat.jpg"):
                name = file.split("_")[0]
                madeArray.append(name)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4"):
                filesArray.append((os.path.join(root,file), file))
            if file.endswith(".avi"):
                filesArray.append((os.path.join(root,file), file))
            if file.endswith(".mkv"):
                filesArray.append((os.path.join(root,file), file))
    for file in filesArray:
        filename = file[1].split(".")[0]
        if filename in madeArray:
            print ("Already processed. Moving along.")
        else:
            print ("Starting to process file " + filename + ".")
            makePicture(file[0], filename)

def usage():
    print ("-i or --input: Input file name")
    print ("-o or --output: Output file name without extension")
    print ("-v or --verbose: Verbose/debug mode")
    print ("--width and --height: width and height of the picture")
    print ("-h or --help: Shows usage of arguments")

def main(argv):
    global VERBOSE, PICTURE_WIDTH, PICTURE_HEIGHT
    input = ""
    output = ""
    directory = ""
    try:
        opts, args = getopt.getopt(argv, "d:hi:o:v", ["directory=","help", "input=", "output=", "verbose", "width", "height"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--verbose"):
            VERBOSE = True
        elif opt in ("-i", "--input"):
            input = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-d", "--directory"):
            directory = arg
        elif opt in ("--width"):
            PICTURE_WIDTH = int(arg)
        elif opt in ("--height"):
            PICTURE_HEIGHT = int(arg)
    if (len(output) == 0 or len(input) == 0) and len(directory) == 0:
        print ("Invalid arguments!")
        print opts
        usage()
        sys.exit()
    else:
        #getAudio(input)
        if len(directory) == 0:
            makePicture(input, output)
        else:
            getMovieFiles(directory)


#makeTestVideo()
main(sys.argv[1:])