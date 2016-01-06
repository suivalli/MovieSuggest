__author__ = 'suidov'

import movieDB

MORE = True

def movieInput():
    movie = raw_input('Enter a movie name: ')
    try:
        movieId = int(movie)
        name = movieDB.getName(movieId)
        if name is not None:
            return [(movieId, name)]
        else:
            return []
    except ValueError:
        return movieDB.getSimilarMovieNameAndIDs(movie)

def getBestMovies(distances):
    sortedDist = distances[:]
    sortedDist.sort()
    first = distances.index(sortedDist[2])
    second = distances.index(sortedDist[3])
    third = distances.index(sortedDist[4])
    fourth = distances.index(sortedDist[5])
    fifth = distances.index(sortedDist[6])
    sixth = distances.index(sortedDist[7])
    seventh = distances.index(sortedDist[8])
    eight = distances.index(sortedDist[9])
    ninth = distances.index(sortedDist[10])
    tenth = distances.index(sortedDist[11])
    return (first, second, third, fourth, fifth, sixth, seventh, eight, ninth, tenth)

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
    return (movies[indexes[0] + 1], movies[indexes[1] + 1], movies[indexes[2] + 1], movies[indexes[3] + 1], movies[indexes[4] + 1],
            movies[indexes[5] + 1], movies[indexes[6] + 1], movies[indexes[7] + 1], movies[indexes[8] + 1], movies[indexes[9] + 1])

def main():
    global MORE
    while MORE:
        found = movieInput()
        movieID = 0
        movieName = ""
        if len(found) == 0:
            print "Found no movies with that name. Please try again"
        elif len(found) == 1:
            print "Found '" + found[0][1] + "', ID: " + str(found[0][0]) + ". Searching for recommendations."
            print ""
            movieID = found[0][0]
            movieName = found[0][1]
        elif len(found) > 1:
            print "Found " + str(len(found)) + " movies. Please choose the number from below and press enter."
            for i in range(0,len(found)):
                print str(i+1) + ") " + found[i][1]
            index = raw_input("Please give the number: ")
            index = int(index) - 1
            movieID = found[index][0]
            movieName = found[index][1]
            print "Searching for recommendations."
            print ""
        if len(found) > 0:
            recommendations = findRecommendations(movieID)
            for i in range(0,len(recommendations)):
                name = movieDB.getName(recommendations[i])
                genres = movieDB.getGenres(recommendations[i])
                gStr = ""
                for genre in genres:
                    gStr += genre + ", "
                gStr = gStr[:-2]
                print "Recommendation nr." + str(i + 1) + ": '" + name + "'."
                print "ID: " + str(recommendations[i])
                print "Genres: " + gStr
                print "--------------------------------"
        print ""
        print "Do you want to search for another movie?"
        yorn = raw_input("Type 'y' or 'n' and press enter.")
        if yorn != 'y':
            MORE = False
        print ""

main()
