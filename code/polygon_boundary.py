#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import drawSvg as draw

class PolygonBoundary():
    def __init__(self, pivots,
                 duration, framerate,
                 colour = "#000000",
                 opacity = 0.5,
                 center = (0,0), phi = 0,
                 theme = {}):
        self.obj_name = "polygon_boundary"
        
        self.pivots = pivots
        self.duration = duration
        self.framerate = framerate
        
        self.compute_inner_points()
        
        self.frames = [{} for i in range(duration)]
    
    def compute_inner_points(self, debug = False):
        n_sides = len(self.pivots) 
        points_per_side = self.duration // n_sides
        remainder = self.duration % n_sides
        if debug:
            print(f"points_per_side={points_per_side} \t n_sides={n_sides} \t remainder={remainder}")
        n_points_per_side = [points_per_side for i in range(n_sides)]
        indexes = np.arange(0,n_sides)
        np.random.shuffle(indexes)
        if debug:
            print(n_points_per_side,indexes)
        for i in indexes[:remainder]:
            n_points_per_side[i] += 1
        if debug:
            print(n_points_per_side,remainder)
        
        if debug:
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
        
    def draw_pivots(self):
        pass
        
        
if __name__ == "__main__":
    p = PolygonBoundary([(0,0),(1,2),(-1,1)], 4, 60)
    print(p.inner_points)