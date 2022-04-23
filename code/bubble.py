#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 22:35:23 2022

@author: j
"""

import numpy as np
from colour_library import linear_gradient, RGB_to_hex, random_palette, hsv_palette_generator
from random import random

class Bubble():
    def __init__(self, start, end, duration, framerate = 60,
                 peak_start = 0.2, peak_end = 0.8, 
                 opacity_min = 0, opacity_max = 0.6, 
                 start_colour = "#ff0000", end_colour = "#0000ff",
                 start_radius = 10, end_radius = 50,
                 movement_path = "cubic"):
        self.obj_name = "bubble"
        self.colours = linear_gradient(start_colour, 
                                       end_colour, 
                                       duration * framerate,
                                       )["hex"]
        
        self.start = start
        self.end = end
        self.duration = duration
        self.framerate = framerate
        self.is_moving = True
        self.movement_path = movement_path
        
        self.peak_start = peak_start
        self.peak_end = peak_end  
        
        self.opacity_min = opacity_min
        self.opacity_max = opacity_max
        
        self.points_between = self.gen_params(movement_path)
        
        self.path = self.calc_positions()
        self.opacity = self.calc_opacity()
        self.radius = self.calc_radius(start_radius, end_radius)
        
    def rand_float_range(self, a, b):
        return a + random()*(b-a)
    
    def random_point_between(self, P1, P2):
        P3 = (self.rand_float_range(min(P1[0], P2[0]), max(P1[0], P2[0])),
              self.rand_float_range(min(P1[1], P2[1]), max(P1[1], P2[1])) )
        return P3
        
    def gen_params(self, movement_path = "cubic"):
        if movement_path == "cubic":
            P0 = self.start
            P3 = self.end
            
            P1 = self.random_point_between(P0,P3)
            P2 = self.random_point_between(P1,P3)
                        
            return (P1,P2)
        pass
    
    def calc_positions(self):
        t_temps = np.linspace(0, 1, self.duration)
        if self.movement_path == "cubic":
            x_coordinates = ((1-t_temps)**3*self.start[0] +
                        3*(1-t_temps)**2*t_temps*self.points_between[0][0] +
                        3*(1-t_temps)*t_temps**2*self.points_between[1][0] +
                        t_temps**3*self.end[0])
            y_coordinates = ((1-t_temps)**3*self.start[1] +
                        3*(1-t_temps)**2*t_temps*self.points_between[0][1] +
                        3*(1-t_temps)*t_temps**2*self.points_between[1][1] +
                        t_temps**3*self.end[1])
                        
        return (x_coordinates,y_coordinates)
    
    def calc_radius(self, start_radius, end_radius):
        t_temps = np.linspace(0, 1, self.duration)
        return list(start_radius + t_temps * (end_radius - start_radius)) 
    
    def calc_opacity(self):
        start_frame_0 = 0
        start_frame_1 = int(np.ceil(self.duration * self.peak_start))
        
        end_frame_0 = int(np.ceil(self.duration * self.peak_end))
        end_frame_1 = int(np.ceil(self.duration))
        
        duration_fadein = start_frame_1 - start_frame_0 + 1
        duration_fadeout = end_frame_1 - end_frame_0 + 1
        
        duration_inner = (int(self.duration) - 
                        duration_fadein - duration_fadeout)
        
        opacity_fadein = list(np.linspace(self.opacity_min,self.opacity_max,duration_fadein))
        opacity_inner = list(np.repeat(self.opacity_max,duration_inner))
        opacity_fadeout = list(np.linspace(self.opacity_max,self.opacity_min,duration_fadeout))
        
        opacity_total = opacity_fadein
        opacity_total += opacity_inner
        opacity_total += opacity_fadeout
        
        return opacity_total
