#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 22:36:35 2022

@author: j
"""

import numpy as np
from background import Background
from random import random, randint
from bubble import Bubble
from polygon import Polygon
from polygon_boundary import PolygonBoundary
from colour_library import  RGB_to_hex

class Animated_object():    
    def __init__(self,
                 duration, 
                 start_time,
                 total_duration = 10,
                 frame_rate = 60,
                 object_type = "bubble",
                 theme = {}):
        """
        Parameters
        ----------
        duration : INT
            total number of frames of the animated object.
        start_time : TYPE
            animation frame start number.
        total_duration : TYPE, optional
            total animation duration in seconds. The default is 10.
        frame_rate : TYPE, optional
            frame rate of the animation. The default is 60.
        object_type : TYPE, optional
            Type of the animated object. The default is "bubble".
        theme : TYPE, optional
            dictionary of the theme parameters for the theme. The default is {}.

        Returns
        -------
        None.

        """        
        self.frames = [{} for i in range(int(np.ceil(total_duration * frame_rate)))]
        
        if object_type == "background":
            colour = theme["start_colour"]
            the_object = Background(duration,
                                    frame_rate,
                                    colour
                                    )       
        
        if object_type == "bubble":
            if not "start_position" in theme:
                start_position = (randint(-500,500),
                                  randint(-500,500))
            else:
                start_position = theme["start_position"]
            
            if not "end_position" in theme:
                end_position = (randint(-500,500),
                                  randint(-500,500))
            else:
                end_position = theme["end_position"]
            
            if not "start_colour" in theme:
                start_colour = RGB_to_hex([randint(0,255),
                                           randint(0,255),
                                           randint(0,255)])
            else:
                start_colour = theme["start_colour"]
            
            if not "end_colour" in theme:
                end_colour = RGB_to_hex([randint(0,255),
                                           randint(0,255),
                                           randint(0,255)])
            else:
                end_colour = theme["end_colour"]
                
            if not "start_radius" in theme:
                start_radius = randint(5,70)
            else:
                start_radius = theme["start_radius"]
                
            if not "end_radius" in theme:
                end_radius = randint(5,70)
            else:
                end_radius = theme["end_radius"]
                
            if not "peak_start" in theme:
                peak_values = [random(), random()]
                peak_start = 0.2 #min(peak_values)
                peak_end = 0.8 # max(peak_values)
            else:
                peak_start = theme["peak_start"]
                peak_end = theme["peak_end"]
                
            if not "opacity_min" in theme:
                opacity_values = [random(), random()]
                opacity_min = 0.0 #min(opacity_values)
                opacity_max = 0.6 # max(opacity_values)
            else:
                opacity_min = theme["opacity_min"]
                opacity_max = theme["opacity_max"]
            
            the_object = Bubble(start_position,
                                end_position,
                                duration,
                                
                                framerate = frame_rate,
                                peak_start = peak_start, peak_end = peak_end, 
                                opacity_min = opacity_min, opacity_max = opacity_max, 
                                start_colour = start_colour, end_colour = end_colour,
                                start_radius = start_radius, end_radius = end_radius,
                                movement_path = "cubic"
                                )
            
        if object_type == "polygon":
            colour = theme["start_colour"]
            opacity = theme["start_opacity"]
            n_objects = theme["n_sides"]
            radius = theme["radius"]
            phi = theme["phi"]
                      
            
            the_object = Polygon(
                n_objects, radius,
                duration, frame_rate,
                colour,
                opacity,
                phi = phi
                )
        
        if object_type == "polygon_boundary":
            pass
        
        
        self.the_object = the_object
        
        # Check that duration value is valid
        assert duration <= total_duration * frame_rate, "Animation of the object is longer than the total animation duration"
        
        # Check that animation overflows
        overflow = False
        if duration + start_time > np.ceil(total_duration * frame_rate):
            overflow = True            
        
        if not overflow:
            start_frame = int(np.ceil(start_time))
            end_frame = int(np.ceil(start_frame + duration - 1))
            
            padded_frame = 0
        else:
            start_frame = int(np.ceil(start_time))
            end_frame = int(np.ceil(total_duration * frame_rate)) - 1
            
            start_frame_0 = 0
            end_frame_0 = int(np.ceil(duration - (end_frame - start_frame) - 1))
            
            padded_frame = end_frame - start_frame + 1
             
        count = 0
        for i in range(start_frame, end_frame + 1):
            self.frames[i]["object"] = the_object.obj_name
            self.frames[i]["frame"] = count
            self.frames[i]["colour"] = the_object.colours[count]
            
            if the_object.obj_name == "bubble":
                self.frames[i]["opacity"] = the_object.opacity[count]
                self.frames[i]["radius"] = the_object.radius[count]
                self.frames[i]["position"] = (the_object.path[0][count],
                                     the_object.path[1][count])
            
            if the_object.obj_name == "polygon":
                self.frames[i]["opacity"] = the_object.opacity[count]
                self.frames[i]["pivot_points"] = the_object.pivot_points
            
            count = count + 1
                
        if padded_frame > 0:
            for i in range(start_frame_0, end_frame_0):
                self.frames[i]["object"] = the_object.obj_name
                self.frames[i]["frame"] = count
                self.frames[i]["colour"] = the_object.colours[count]
                
                if the_object.obj_name == "bubble":
                    self.frames[i]["opacity"] = the_object.opacity[count]
                    self.frames[i]["radius"] = the_object.radius[count]
                    self.frames[i]["position"] = (the_object.path[0][count],
                                         the_object.path[1][count])
                    
                if the_object.obj_name == "polygon":
                    self.frames[i]["opacity"] = the_object.opacity[count]
                    self.frames[i]["pivot_points"] = the_object.pivot_points
                    
                count = count + 1
