# Suggesting movies based on it's fingerprint

The main idea of this project is to recommend movies by their fingerprints.

## What we mean by fingerprint?

We took a frame for each second of a movie, found the dominant color of it and added it to the array. This concluded in a picture that is 3840 pixels wide and 1 pixel high. You can see a fingerprint of Matrix [here](http://imgur.com/lZ0J7tH). This is the fingerprint times 2160 to make an UHD wallpaper.

## How to see the recommendations?

* Download the repository as .zip, extract it.
* Go to root directory of repository (you should see getRecommendations.py file there.
* Open up a command line (In Windows, hold Shift and right-click in the directory, Choose "Open command window here"
* Write to the opened window ```python getRecommendations.py```
* Follow the instructions - you can either insert a movie name, part of the name or a movie ID (you can see the movie ID's from the folder pics in the repository)
* Watch a recommended movie!

## Where can I get the nice wallpapers?
All of the movie wallpapers are held in [here](https://www.dropbox.com/s/630vhmtf0mftcgs/origPics.zip?dl=0). Every movie has 3 files:
* File ending with _dat is a data file meant for use in comparing the movies
* File ending with _orig is 2160 pixels high and the width depends on the movie length
* File without underscore ending is a resized version of _orig picture and is 3840*2160 pixels.
