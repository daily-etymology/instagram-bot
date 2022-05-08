# Elements folder
This folder contains the fundamental building blocks used for the animation.


## `background.py`
A very simple file with a class that stores information about the background
colour. Currently it only supports static colour

## `bubble.py` 
This file stores a class that keeps track of the information of each bubble 
that is drawn on the screen.

## `polygon.py` 
File to which computes pivot points of the polygon and the inner points, which
are used later when drawing the main regular on the screen. In theory it is 
possible to move the polygon to the other part of the screen, but I did not 
test it, as I hardcoded the image resolution values. This class also computes
locations of the text boxes such that they are contained within the polygon
boundaries.

## `polygon_boundary`
The `polygon_boundary.py` is an implicit child of `polygon.py` and manages
animation of the snake (or some other animation) around the boundary of the
polygon. I did not expose its settings, but you can play around with parameters
such as colour of the snake and time it takes to desolve into the background.

## `rectangle.py`
A file with a rectangle class that can be used when you want to draw a 
rectangle on the screen. Only supports constants opacity and colour values.

## `text_box.py`
This script manages computation of the text flow in a textbox. I implemented a
simple greedy line-break algorithm and a more advanced TeX minimal sum of 
squares dynamic programming technique. However, I found that maximisation of 
the maximal font size yields the best looking results.
