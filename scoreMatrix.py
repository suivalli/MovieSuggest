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

def getScore(pic1,pic2):
    distanceSum = getDistanceSum(pic1,pic2) - 39000
    changes1 = getNumTransforms(pic1)
    changes2 = getNumTransforms(pic2)
    score = distanceSum - 10 * (abs(changes1 - changes2))
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

def getBestMovies(distances):
    sortedDist = distances[:]
    sortedDist.sort()
    first = distances.index(sortedDist[2])
    second = distances.index(sortedDist[3])
    third = distances.index(sortedDist[4])
    fourth = distances.index(sortedDist[5])
    fifth = distances.index(sortedDist[6])
    return (first, second, third, fourth, fifth)

def findRecommendations(MovieID):
    f = open("data/matrix.csv", 'r')
    header = True
    for row in f:
        if header:
            header = False
            movies = row.split("\t")
        if not header:
            recomm = row.split("\t")
            if recomm[0] == str(MovieID):
                indexes = getBestMovies(recomm[1:])
                break
    return (movies[indexes[0] + 1], movies[indexes[1] + 1], movies[indexes[2] + 1], movies[indexes[3] + 1], movies[indexes[4] + 1])

#writeDistanceMatrix(getPics())
#print getNumTransforms('pics/Pirates of the Caribbean On Stranger Tides_dat.jpg')
#print findRecommendations('Sin City')