# visuals folder
This folder contains all the scripts used to generate animation frames.

## elements folder
The `elements` folder contains scripts of the fundamental visual objects used 
for the animation. 

## helpers folder
The `helpers` folder contains helpful scripts to do colour transformations and
handle the text flowing logic.

## `animated_object.py`
This is the core file used in all animations. It is built on top of a simpe
idea. Each animated object is completly independent. Only things that matter
are, duration of the animated object, and when it first appears on the screen.
For example, if total duration of the animation is 10 seconds, and animated 
object is 7 seconds long and it starts on the 4th second. We can think of this
animated object in two parts: 1. It appears at 4 and goes up to 10, then 2.
it again appears at 1 and goes up to 2. This class computes progress of the 
animated object for each frame of the animation.

## `display.py`
The `display.py` file aggregates all the visible objects. Here you can find
the `self.theme` dictionary that can be used to adjust the theme used for the 
animation. There is a need to re-organise this file to make it more robust as
at the moment it is quite long and not very intuitive.

## `post_layout.py`
This file manages layout of the text boxes and text within. Currently all
locations are hadrcoded, but it would be very cool relative positions were used
instead.
