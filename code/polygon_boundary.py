#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import drawSvg as draw
from colour_library import gen_rainbow

class PolygonBoundary():
    def __init__(self, pivots,
                 duration, framerate,
                 n_repeats,
                 total_duration = 10,
                 theme = {}):
        self.obj_name = "polygon_boundary"
        
        self.pivots = pivots
        self.duration = duration
        self.framerate = framerate
        self.total_duration = total_duration
        self.n_repeats = n_repeats
        
        self.compute_inner_points()
        
        self.theme = theme
        self.particles = self.gen_particles()
    
    def compute_inner_points(self, debug = False):
        n_sides = len(self.pivots) 
        points_per_side = (self.duration * self.framerate) // n_sides
        remainder = self.duration % n_sides            
        n_points_per_side = [points_per_side for i in range(n_sides)]
        indexes = np.arange(0,n_sides)
        np.random.shuffle(indexes)
        if debug:
            print(f"points_per_side={points_per_side} \t n_sides={n_sides} \t remainder={remainder}")
            print(n_points_per_side,indexes)
        for i in indexes[:remainder]:
            n_points_per_side[i] += 1
        if debug:
            print(n_points_per_side,remainder)
            print()
        
        self.inner_points = []
        for i in range(n_sides):
            tmp_points = []

            tmp_points = np.linspace(self.pivots[i],
                              self.pivots[(i+1) % n_sides],
                              n_points_per_side[i] + 1)

            for point in tmp_points[:-1]:
                self.inner_points.append(list(point))
        
        if debug:
            print(self.inner_points)
            print()
        
    def gen_particles(self):
        particles = []
        one_loop_duration = self.total_duration / self.n_repeats
        
        print(f"boundary repeats: {self.n_repeats} \t time per iteration {one_loop_duration}")
        
        if "style" in self.theme.keys():
            if self.theme["style"] == "pivot_only":
                for repeat_number in range(self.n_repeats):
                    for c, pivot in enumerate(self.pivots):
                        tmp = {
                            "object_type" : "bubble",
                            "start_position" : pivot,
                            "end_position" : pivot,
                            "start_colour" : "#000000",
                            "end_colour" : "#ff00ff",
                            "start_radius" : 0,
                            "end_radius" : 10,
                            "peak_start" : 0.0,
                            "peak_end" : 0.8,
                            "opacity_min" : 0.0,
                            "opacity_max" : 0.6,
                            
                            "duration" : 2,
                            "start_time" : repeat_number * one_loop_duration +  c * one_loop_duration * 1 / len(self.pivots)
                            }
                        particles.append(tmp)
            if self.theme["style"] == "pivot_and_inner":
                number_of_colours = int(np.ceil(self.n_repeats * len(self.inner_points)))
                colours = gen_rainbow(number_of_colours)
                for repeat_number in range(self.n_repeats):
                    for c, inner_point in enumerate(self.inner_points):
                        tmp = {
                            "object_type" : "bubble",
                            "start_position" : inner_point,
                            "end_position" : inner_point,
                            "start_colour" : colours[repeat_number * len(self.inner_points) + c],
                            "end_colour" : "#ffffff", #colours[repeat_number * len(self.inner_points) + c],
                            "start_radius" : 8,
                            "end_radius" : 0,
                            "peak_start" : 0.0,
                            "peak_end" : 0.8,
                            "opacity_min" : 1.0,
                            "opacity_max" : 1.0,
                            
                            "duration" : 1,
                            "start_time" : repeat_number * one_loop_duration +  c * one_loop_duration / (len(self.inner_points))
                            }
                        particles.append(tmp)
        return particles
                    
        
        
if __name__ == "__main__":
    p = PolygonBoundary([(0,0),(1,2),(-1,1)], 4, 1,
                        theme = {"style":"pivot_only"})
    print(p.inner_points)