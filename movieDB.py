import sqlite3
import csv
import os

#DO NOT PUT THE FLAG TO TRUE IF YOU DON't WANT TO CREATE ALL OF THE DB AGAIN!
CREATING = True

conn = sqlite3.connect("data\movies.db")

conn.text_factory = str

c = conn.cursor()

def getPicNames():
    filesArray = []
    for root, dirs, files in os.walk("pics"):
        for file in files:
            if file.endswith("_dat.jpg"):
                filesArray.append(file.split("_")[0])
    return filesArray

pics =  getPicNames()

if CREATING:
    movieCreate = 'CREATE TABLE IF NOT EXISTS MOVIES ' \
                  '(' \
                  'ID INTEGER, NAME TEXT, GENRES TEXT' \
                  ')'

    ratingsCreate = 'CREATE TABLE IF NOT EXISTS RATINGS ' \
                    '(' \
                    'MOVIEID INTEGER, RATING REAL' \
                    ')'

    tagsCreate = 'CREATE TABLE IF NOT EXISTS TAGS' \
                 '(' \
                 'MOVIEID INTEGER, TAG TEXT' \
                 ')'

    c.execute(movieCreate)
    c.execute(ratingsCreate)
    c.execute(tagsCreate)

    conn.commit()

    with open('movies.csv','rb') as csvfile:
        read = csv.reader(csvfile, delimiter=",")
        rows = []
        count = 0
        for row in read:
            if count != 0:
                if row[0] in pics:
                    rows.append((int(row[0]), row[1], row[2]))
            count += 1
        c.executemany('INSERT INTO MOVIES VALUES (?,?,?)', rows)
        conn.commit()


    with open('ratings.csv', 'rb') as csvfile:
        read = csv.reader(csvfile, delimiter=",")
        rows = []
        count = 0
        for row in read:
            if count != 0:
                if row[1] in pics:
                    movieID = int(row[1])
                    rating = float(row[2])
                    rows.append((movieID, rating))
            count += 1
        c.executemany('INSERT INTO RATINGS VALUES (?,?)', rows)
        conn.commit()

    with open('tags.csv', 'rb') as csvfile:
        read = csv.reader(csvfile, delimiter=",")
        rows = []
        count = 0
        for row in read:
            if count != 0:
                if row[1] in pics:
                    movieID = int(row[1])
                    tag = row[2]
                    rows.append((movieID, tag))
            count += 1
        c.executemany('INSERT INTO TAGS VALUES (?,?)', rows)
        conn.commit()


def getAvgRating(MovieID):
    t = (str(MovieID),)
    c.execute('SELECT AVG(RATING) FROM RATINGS WHERE MOVIEID = ?', t)
    avg = c.fetchone()
    return avg[0]

def getGenres(MovieID):
    t = (str(MovieID),)
    c.execute('SELECT GENRES FROM MOVIES WHERE ID = ?', t)
    genres = c.fetchone()[0]
    return genres.split("|")

def getTags(MovieID):
    t = (str(MovieID),)
    c.execute('SELECT DISTINCT TAG FROM TAGS WHERE MOVIEID = ?', t)
    tags = c.fetchall()
    tagArr = []
    for row in tags:
        tagArr.append(row[0])
    return tagArr

def getName(MovieID):
    t = (str(MovieID),)
    c.execute('SELECT NAME FROM MOVIES WHERE ID = ?', t)
    return c.fetchone()[0]

def getRatingCount(MovieID):
    t = (str(MovieID),)
    c.execute('SELECT COUNT(1) FROM RATINGS WHERE MOVIEID = ?', t)
    return c.fetchone()[0]

def getSimilarMovieNameAndIDs(MovieName):
    t = (MovieName.lower(),)
    c.execute('SELECT ID, NAME FROM MOVIES WHERE LOWER(NAME) LIKE ?', '%' + t + '%')
    possibleNames = c.fetchall()
    nameArr = []
    for row in possibleNames:
        nameArr.append((row[0], row[1]))
    return nameArr

#print getAvgRating(1)
#print getGenres(1)
#print getTags(100)
#print getName(4816)
#print getRatingCount(588)
#print getSimilarMovieNameAndIDs("Toy")

conn.close()