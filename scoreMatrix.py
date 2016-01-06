import os
import cv2
import numpy as np

def getPics():
    filesArray = []
    for root, dirs, files in os.walk("pics"):
        for file in files:
            if file.endswith("_dat.jpg"):
                filesArray.append(os.path.join(root,file))
    return filesArray

def getNumTransforms(pic):
    img = cv2.imread(pic)
    count = 0
    for i in range(0,3839):
        if getEuclidDistance(img[0][i], img[0][i+1]) > 15.75:
            count += 1
    return count

def getEuclidDistance(color1, color2):
    dist = np.linalg.norm(color1 - color2)
    return dist

def getDistanceSum(pic1, pic2):
    img1 = cv2.imread(pic1)
    img2 = cv2.imread(pic2)
    sum = 0
    for i in range(0,3840):
        sum += getEuclidDistance(img1[0][i],img2[0][i])
    return sum

def getChannelSums(pic):
    img = cv2.imread(pic)
    r, g, b = 0, 0, 0
    for i in range(0,3840):
        r += img[0][i][2]
        g += img[0][i][1]
        b += img[0][i][0]
    return [r,g,b]

def sameDominantColor(dic1, dic2):
    dic1Dom = dic1.index(max(dic1))
    dic2Dom = dic2.index(max(dic2))
    if dic1Dom == dic2Dom:
        return True
    else:
        return False


def getScore(pic1,pic2):
    distanceSum = getDistanceSum(pic1,pic2) - 39000
    chSum1 = getChannelSums(pic1)
    chSum2 = getChannelSums(pic2)
    same = sameDominantColor(chSum1, chSum2)
    changes1 = getNumTransforms(pic1)
    changes2 = getNumTransforms(pic2)
    score = distanceSum - 10 * (abs(changes1 - changes2))
    if same:
        score -= 150
    return score

def writeDistanceMatrix(pics):
    f = open("data/matrix.csv", 'w')
    row = "\t"
    for i in range(0,len(pics)):
        row +=  pics[i].split("\\")[1].split("_")[0] + "\t"
    row += "\n"
    f.write(row)
    for i in range(0,len(pics)):
        row = pics[i].split("\\")[1].split("_")[0] + "\t"
        print "Doing row number " + str(i+1)
        for j in range(0,len(pics)):
            row += str(getScore(pics[i],pics[j])) + "\t"
        row += "\n"
        f.write(row)
    f.close()



#writeDistanceMatrix(getPics())
#print getNumTransforms('pics/Pirates of the Caribbean On Stranger Tides_dat.jpg')
#print findRecommendations('Sin City')