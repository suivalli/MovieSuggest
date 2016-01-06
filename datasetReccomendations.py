import csv
import movieDB
import scoreMatrix
from collections import defaultdict
import operator
import random


def getUserRatings():
    pics = movieDB.getPicNames()

    with open('ratings1.csv', 'rb') as csvfile:
        read = csv.reader(csvfile, delimiter=",")
        ratings = defaultdict(dict)
        users = defaultdict(dict)
        for row in read:
            if row[1] in pics:
                ratings[row[1]][row[0]] = float(row[2])
                users[row[0]][row[1]] = float(row[2])
    return ratings, users

def getRecommendedMovies(movieID):
    votedUsers = []

    for k,v in ratings[movieID].iteritems():
        if v >= 0.0:
            votedUsers.append(k)

    finalRatings = defaultdict(list)
    for user in votedUsers:
        for k1,v1 in users[user].iteritems():
            if k1 != movieID:
                finalRatings[k1].append(abs(v1-users[str(user)][str(movieID)]))

    average = defaultdict(float)
    for k,v in finalRatings.iteritems():
        average[k] = sum(v)/len(v)

    return sorted(average.items(), key=operator.itemgetter(1), reverse=False)

def getAllRatingReccomendations():
    pics = movieDB.getPicNames()
    recc = defaultdict(list)
    for movie in pics:
        recc[movie] = [k for k,v in getRecommendedMovies(movie)]
    return recc

def getAllOurReccomendations():
    pics = movieDB.getPicNames()
    recc = defaultdict(list)
    for movie in pics:
        recc[movie] = list(scoreMatrix.findRecommendations(movie))
    return recc

def evaluateFitness(listIndices, ourRecc, ratingRecc):
    result = []
    for k,v in ourRecc.iteritems():
        result.append(len(list(set(ourRecc[k]) & set([ratingRecc[k][i] for i in listIndices]))))
    finalres = [i for i in result if i > 0]
    return len(finalres), max(finalres), sum(finalres)

def printRecommendedMovies(movieID):
    result = getRecommendedMovies(movieID)
    for k in result:
        print movieDB.getName(int(k[0]))

ratings, users = getUserRatings()

allourrecc = getAllOurReccomendations()
allratingrecc = getAllRatingReccomendations()

evaluateFitness(range(47,58), allourrecc, allratingrecc)

maximumval = (0, 0, 0)
bestrand = []
for i in range(0,100000):
    rand = random.sample(range(198), 10)
    res = evaluateFitness(rand, allourrecc, allratingrecc)
    if res[2] > maximumval[2]:
        bestrand = rand
        maximumval = res
print maximumval, bestrand




''' USELESS

def doValidateAll():
    pics = movieDB.getPicNames()
    result, count, ourPrediction = [], 0, []
    for movie in pics:
        count += 1
        print count
        ours = scoreMatrix.findRecommendations(movie)
        dataset = [i[0] for i in getRecommendedMovies(movie)]
        result.append(len(list(set(ours) & set(dataset))))
        ourPrediction.append(ours)
        print ours, dataset
    return result, ourPrediction

result = sorted(averages.items(), key=operator.itemgetter(1), reverse=True)[indiceList]
datasetRecc = [i[0] for i in result]
result.append(len(list(set(ours) & set(dataset))))


results, our = doValidateAll()

final = [i for i in results if i > 0]
print len(final), max(final), sum(final)

def tryRandom(compare):
    movies = movieDB.getPicNames()
    res = []
    for resultset in compare:
        rand = [movies[i] for i in random.sample(range(199), 10)]
        res.append(len(list(set(resultset) & set(rand))))
    finalres = [i for i in res if i > 0]
    return len(finalres), max(finalres), sum(finalres)

print tryRandom(our)

max([len(v) for k,v in b.iteritems()])
'''

