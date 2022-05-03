#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

# https://geostat-framework.readthedocs.io/projects/gstools/en/stable/examples/04_vector_field/00_2d_vector_field.html
import gstools as gs  # Random field package

from random import randint
from visuals.helpers.colour_library import  RGB_to_hex, hsv_palette_generator, invert_colour

from visuals.animated_object import Animated_object
from visuals.elements.polygon_boundary import PolygonBoundary
from visuals.post_layout import PostLayout

    
class Display():
    def __init__(self,
                 duration = 10,
                 frame_rate = 60):
        
        self.theme = {
            "background" : {
                # If None, then default to the first colour in palette
                # [R, G, B]
                "colour" : np.random.sample([0, 0, 0], [255, 255, 255]),
                },
            "bubble" : {
                "n_max" : 50,
                "n_min" : 2,
                "duration_min" : 2,
                "duration_max" : 10,
                "radius_range" : [10, 300],
                "start_position_range" : [-500, 500],
                "peak_start" : 0.2,
                "peak_end" : 0.8,
                "opacity_min" : 0,
                "opacity_max" : 0.6
                },
            "polygon" : {
                "n_sides_max" : 9,
                "n_sides_min" : 5,
                "start_opacity" : 0.5,
                "radius" : 500,
                "phi" : 5 * np.pi / 2,
                "start_colour" : None
                },
            "polygon_boundary" : {
                "style":"pivot_and_inner"
                },
            "textbox" : {
                "box_colour" : "#ff00ff",
                "box_opacity" : 0.0,
                "text_colour" : None,
                "peak_start" : 0.2,
                "peak_end" : 0.8,
                "opacity_min" : 0,
                "opacity_max" : 0.6
                },
            "field" : {
                # a smooth Gaussian covariance model
                "surface" : gs.SRF(gs.Gaussian(dim=2, var=1, len_scale=10),
                                   generator="VectorField"),
                "vector" : None,
                "vector_range" : [-5, 5]
                },
            "colours" : {
                "n_colours_in_palette" : 5
                }
            }
        
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
                             "polygon_boundary",
                             "rectangle",
                             "textbox"
                             ]
                        
        n_sides = np.random.randint(self.theme["polygon"]["n_sides_min"],
                                    self.theme["polygon"]["n_sides_max"])
        if n_sides == 9:
            n_sides = 50
            
        self.theme["polygon"]["n_sides"] = n_sides
        
        print(f"n_sides: {n_sides}")
        #palettes = random_palette(5)
        palettes = hsv_palette_generator(self.theme["colours"]["n_colours_in_palette"])
        self.theme["colours"]["palettes"] = palettes
        
        objects = []
        if self.theme["background"]["colour"] is None:
            bg_colour = palettes[0]
        else:
            assert type(self.theme["background"]["colour"]) == list, "bg colour should be in [R, G, B] form"
            bg_colour = self.theme["background"]["colour"]
        b = Animated_object(duration = self.duration, 
                            start_time = 0, 
                            object_type = "background",
                            theme = {"start_colour":RGB_to_hex(
                                bg_colour
                                )})
        objects.append(b)
        
        palettes = palettes[1:]
        
        
        MIN_BUBBLES = self.theme["bubble"]["n_min"]
        MAX_BUBBLES = self.theme["bubble"]["n_max"]
        
        n_bubble = randint(MIN_BUBBLES, MAX_BUBBLES)
        
        self.theme["bubble"]["n"] = n_bubble
        
        #n_bubble = 25
        
        x0 = MIN_BUBBLES
        x1 = MAX_BUBBLES
        y0 = 50
        y1 = 200
                
        bubble_scalor = self.compute_bubble_speed(n_bubble, x0, x1, y0, y1)
        
        if self.theme["field"]["vector"] is None:
            vec_range = self.theme["field"]["vector_range"]
            x_vector_scalor = bubble_scalor * np.random.uniform(min(vec_range),
                                                                max(vec_range))
            y_vector_scalor = bubble_scalor * np.random.uniform(min(vec_range),
                                                                max(vec_range))
        else:
            x_vector_scalor, y_vector_scalor = self.theme["field"]["vector"]
        
        min_duration = self.theme["bubble"]["duration_min"]
        max_duration = self.theme["bubble"]["duration_max"]
        
        if self.theme["bubble"]["radius_range"] is None:
            min_radius = 5  +     (1 - n_bubble/MAX_BUBBLES)
            max_radius = 10 +     MAX_BUBBLES * (1 - n_bubble/MAX_BUBBLES)
        else:
            min_radius = min(self.theme["bubble"]["radius_range"])
            max_radius = max(self.theme["bubble"]["radius_range"])
        
        print("n_bubbles:{}".format(n_bubble))
        print("x_vector_scalor:{:.2f}\ty_vector_scalor:{:.2f}".format(x_vector_scalor,y_vector_scalor))
        print("min_radius:{:.2f}\tmax_radius:{:.2f}".format(min_radius,max_radius))
        print("min_duration:{:.2f}\tmax_duration:{:.2f}".format(min_duration,max_duration))
                
        for i in range(n_bubble):
            col_ids = np.random.choice(np.arange(len(palettes)),2)
            
            # Bubble theme
            # theme = {
            #     "start_colour" : RGB_to_hex(palettes[col_ids[0]]),
            #     "end_colour" : RGB_to_hex(palettes[col_ids[1]]),
            #     "start_radius" : np.random.uniform(min_radius,max_radius),
            #     "end_radius" : np.random.uniform(min_radius,max_radius)
            #     }
            
            theme = self.theme["bubble"]
            theme["start_colour"] = RGB_to_hex(palettes[col_ids[0]])
            theme["end_colour"] = RGB_to_hex(palettes[col_ids[1]])
            theme["start_radius"] = np.random.uniform(min_radius,max_radius)
            theme["end_radius"] = np.random.uniform(min_radius,max_radius)
            
            min_start_pos = min(self.theme["bubble"]["start_position_range"])
            max_start_pos = max(self.theme["bubble"]["start_position_range"])
            
            theme["start_position"] = (randint(min_start_pos, max_start_pos),
                                      randint(min_start_pos, max_start_pos))
            
            direction_vector = self.theme["field"]["surface"]((
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
            
            self.theme["bubble"] = theme
        
        
        theme = self.theme["polygon"]
        if self.theme["polygon"]["start_colour"] is None:
            theme["start_colour"] = RGB_to_hex(bg_colour)
        theme["n_sides"] = n_sides
        
        
        polygon = Animated_object(duration = self.duration, 
                            start_time = 0, 
                            object_type = "polygon",
                            theme = theme)
        
        self.theme["polygon"] = theme
        
        objects.append(polygon)
        
        # Pivot points of the polygon 
        # used for the polygon boundary
        polygon.the_object.pivot_points
        
        theme = self.theme["polygon_boundary"]
        theme["end_colour"] = RGB_to_hex(bg_colour)
        boundary_0 = PolygonBoundary(polygon.the_object.pivot_points,
                        self.duration, self.frame_rate,
                        n_repeats = 2,
                        total_duration=self.duration,
                        theme = theme
                        )
        
        self.theme["polygon_boundary"] = theme

        for particle in boundary_0.particles:
            b = Animated_object(duration = particle["duration"], 
                                start_time = particle["start_time"], 
                                object_type = particle["object_type"],
                                theme = particle)
            objects.append(b)
                
        post_group = PostLayout(polygon.the_object, self.theme)        
        for obj in post_group.objects:
            b = Animated_object(duration = obj["duration"], 
                                start_time = obj["start_time"],
                                object_type = obj["object_type"],
                                theme = obj["theme"]
                                )
            objects.append(b)
        #polygon.compute_inner_box
        
        # Add text boxes, with text
        
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
