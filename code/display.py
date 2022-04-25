#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 22:39:16 2022

@author: j
"""

import numpy as np

# https://geostat-framework.readthedocs.io/projects/gstools/en/stable/examples/04_vector_field/00_2d_vector_field.html
import gstools as gs  # Random field package

from random import randint
from colour_library import  RGB_to_hex, hsv_palette_generator, invert_colour

from animated_object import Animated_object
from polygon_boundary import PolygonBoundary

class Display():
    def __init__(self,
                 duration = 10,
                 frame_rate = 60):
        
        self.frame_rate = frame_rate
        self.duration = duration
        self.frames = self.combine_objects(self.gen_objects())
        
    def compute_bubble_speed(self, x, x0, x1, y0, y1):
        m = (y0-y1)/(x0-x1)
        c = y0 - m*x0
        
        return x*m + c
    
    def gen_objects(self):
        available_objects = ["background",
                             "bubble",
                             "polygon",
                             "polygon_boundary"]
        
        # a smooth Gaussian covariance model
        model = gs.Gaussian(dim=2, var=1, len_scale=10)
        srf = gs.SRF(model, generator="VectorField")
        
        #palettes = random_palette(5)
        palettes = hsv_palette_generator(4)
        
        objects = []
        bg_colour = [0, 0, 0]#palettes[0]
        b = Animated_object(duration = self.duration, 
                            start_time = 0, 
                            object_type = "background",
                            theme = {"start_colour":RGB_to_hex(
                                bg_colour
                                )})
        objects.append(b)
        
        palettes = palettes[1:]
        
        
        MIN_BUBBLES = 2
        MAX_BUBBLES = 100
        
        n_bubble = randint(MIN_BUBBLES, MAX_BUBBLES)
        
        #n_bubble = 25
        
        x0 = MIN_BUBBLES
        x1 = MAX_BUBBLES
        y0 = 50
        y1 = 200
                
        bubble_scalor = self.compute_bubble_speed(n_bubble, x0, x1, y0, y1)
        
        x_vector_scalor = bubble_scalor * np.random.uniform(-2,2)
        y_vector_scalor = bubble_scalor * np.random.uniform(-2,2)
        
        min_duration = 5
        max_duration = 10
        
        min_radius = 5  +     (1 - n_bubble/MAX_BUBBLES)
        max_radius = 10 +     MAX_BUBBLES * (1 - n_bubble/MAX_BUBBLES)
        
        print("n_bubbles:{}".format(n_bubble))
        print("x_vector_scalor:{:.2f}\ty_vector_scalor:{:.2f}".format(x_vector_scalor,y_vector_scalor))
        print("min_radius:{:.2f}\tmax_radius:{:.2f}".format(min_radius,max_radius))
        print("min_duration:{:.2f}\tmax_duration:{:.2f}".format(min_duration,max_duration))
                
        for i in range(n_bubble):
            col_ids = np.random.choice(np.arange(len(palettes)),2)
            
            # Bubble theme
            theme = {
                "start_colour" : RGB_to_hex(palettes[col_ids[0]]),
                "end_colour" : RGB_to_hex(palettes[col_ids[1]]),
                "start_radius" : np.random.uniform(min_radius,max_radius),
                "end_radius" : np.random.uniform(min_radius,max_radius)
                }
            
            theme["start_position"] = (randint(-500,500),
                                      randint(-500,500))
            
            direction_vector = srf((
                theme["start_position"][0],
                theme["start_position"][1]
                ))
            
            theme["end_position"] = (
                theme["start_position"][0] + x_vector_scalor * direction_vector[0],
                theme["start_position"][1] + y_vector_scalor * direction_vector[1]
                )
            
            duration = int(np.ceil(np.random.uniform(min_duration,
                                         max_duration)))
            start_time = int(np.ceil(np.random.uniform(0,self.duration) ))
            
            b = Animated_object(duration = duration, 
                                start_time = start_time, 
                                object_type = "bubble",
                                theme = theme)
            objects.append(b)
        
        theme = {
            "start_colour" :RGB_to_hex(
                bg_colour
                ), #"#ffffff",  #RGB_to_hex(invert_colour(bg_colour, False))
            
            "start_opacity" : 0.5,
            "n_sides" : np.random.randint(5,30),
            "radius" : 500,
            "phi" : 5 * np.pi / 2
            }
        
        b = Animated_object(duration = self.duration, 
                            start_time = 0, 
                            object_type = "polygon",
                            theme = theme)
        
        objects.append(b)
        
        # Pivot points of the polygon 
        # used for the polygon boundary
        b.the_object.pivot_points
        
        boundary_0 = PolygonBoundary(b.the_object.pivot_points,
                        self.duration, self.frame_rate,
                        n_repeats = 2,
                        total_duration=self.duration,
                        theme = {"style":"pivot_and_inner",
                                 "end_colour" : RGB_to_hex(
                                     bg_colour
                                     )}
                        )

        for particle in boundary_0.particles:
            b = Animated_object(duration = particle["duration"], 
                                start_time = particle["start_time"], 
                                object_type = particle["object_type"],
                                theme = particle)
            objects.append(b)
            
        
        return objects
    
    def combine_objects(self, objects):
        n_frames = self.duration * self.frame_rate
        
        frames = []
        
        for i in range(n_frames):
            frame = []
            for o in objects:
                frame.append(o.frames[i])
            frames.append(frame)
        
        return frames
