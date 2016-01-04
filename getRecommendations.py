__author__ = 'suidov'

import scoreMatrix
import movieDB

MORE = True

def movieInput():
    movie = raw_input('Enter a movie name: ')
    return movieDB.getSimilarMovieNameAndIDs(movie)

def main(argv):
    global MORE
    while MORE:
        found = movieInput()
        movieID = 0
        movieName = ""
        if len(found) == 0:
            print "Found no movies with that name. Please try again"
            movieInput()
        elif len(found) == 1:
            print "Found '" + found[0][1] + "'. Searching for recommendations."
            movieID = found[0][0]
            movieName = found[0][1]
        elif len(found) > 1:
            print "Found " + str(len(found)) + "movies. Please choose the number from below and press enter."
            for i in range(0,len(found)):
                print str(i+1) + "). " + found[i]
            index = raw_input("Please give the number: ")
            index = int(index) - 1
            movieID = found[index][0]
            movieName = found[index][1]
            print "Searching for recommendations."
        if len(found) > 0:
            recommendations = scoreMatrix.findRecommendations(movieID)
            for i in range(0,len(recommendations)):
                name = movieDB.getName(recommendations[i])
                genres = movieDB.getGenres(recommendations[i])
                print "Recommendation nr." + str(i + 1) + ": '" + name + "'."
                print "Genres: " + genres
                print "--------------------------------"
        print "Do you want to search for another movie?"
        yorn = raw_input("Type 'y' or 'n' and press enter.")
        if yorn != 'y':
            MORE = False

