#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Background of the image
"""
import numpy as np

class Background():
    def __init__(self,
                 duration, framerate,
                 colour = "#11aa00",
                 style = "solid"):
        self.obj_name = "background"
                
        self.duration = duration
        self.framerate = framerate
        
        self.colours = self.gen_solid_colour(colour)
        
        self.opacity = np.repeat(1, int(np.ceil(duration*framerate)))
        
    def gen_solid_colour(self, colour):
        return np.repeat(colour, int(np.ceil(self.duration*self.framerate)))
