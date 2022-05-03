#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import drawSvg as draw

class Rectangle():
    def __init__(self, x, y, width, height,
                 duration, framerate,
                 text = "",
                 theme = {}):
        self.obj_name = "rectangle"
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.duration = duration
        self.framerate = framerate
        
        self.theme = theme
        
        self.text = text
        
        if not "box_opacity" in theme.keys():
            self.opacity = 0.6
        else:
            self.opacity = theme["box_opacity"]
            
        if not "box_colour" in theme.keys():
            self.box_colour = "#ffaa66"
        else:
            self.box_colour = theme["box_colour"]
            
        self.colours = np.repeat(self.box_colour, int(np.ceil(duration*framerate)))
        self.opacity = np.repeat(self.opacity, int(np.ceil(duration*framerate)))
        

if __name__ == "__main__":
    rect = Rectangle(0, 0, 10, 100, 1, 60)
    
    print(rect.colours)
    print(rect.opacity)

