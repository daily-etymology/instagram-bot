#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import drawSvg as draw

class Polygon():
    def __init__(self, n_sides, radius,
                 duration, framerate,
                 colour = "#aaaaaa",
                 opacity = 0.5,
                 center = (0,0), phi = 0,
                 clockwise = True):
        self.obj_name = "polygon"
        
        self.clockwise = clockwise
        
        self.duration = duration
        self.framerate = framerate
        
        self.center = center
        self.radius = radius
        self.n_sides = n_sides
        self.phi = phi
        
        self.pivot_points = self.compute_pivot_points()
        self.inner_points = None
        
        self.colours = np.repeat(colour, int(np.ceil(duration*framerate)))
        self.opacity = np.repeat(opacity, int(np.ceil(duration*framerate)))
    
    def compute_pivot_points(self):
        theta = 2 * np.pi / self.n_sides
        
        if self.clockwise:
            theta *= -1
        
        pivot_points = []
        
        for i in range(self.n_sides):
            x_ = self.center[0] + self.radius * np.cos(theta * i)
            y_ = self.center[0] + self.radius * np.sin(theta * i)
            
            x = x_ * np.cos(self.phi) - y_ * np.sin(self.phi)
            y = x_ * np.sin(self.phi) + y_ * np.cos(self.phi)
            
            pivot_points.append([x,y])
        return np.array(pivot_points)
        

if __name__ == "__main__":
    n_sides = 16
    # 4 : pi/2
    # 5 : 3 * pi / 2
    p = Polygon(n_sides,500, phi =  5*np.pi/(2) )
    print(p.pivot_points)
    
    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
        
    d = draw.Drawing(SCREEN_WIDTH, SCREEN_HEIGHT, origin='center', displayInline=False)
    
    # Add lines
    for i in range(len(p.pivot_points)):
        d.append(draw.Lines(0,0,
            p.pivot_points[i-1][0],p.pivot_points[i-1][1],
            p.pivot_points[i][0],p.pivot_points[i][1],
                            close=False,
                    fill='#eeee00', 
                    stroke_width = 2, 
                    #stroke="#eeee00",
                    opacity = 0.5,
                    #stroke_opacity = 0.5
                    ))
        d.append(draw.Line(p.pivot_points[i-1][0], p.pivot_points[i-1][1], 
                           p.pivot_points[i][0], p.pivot_points[i][1],
                    stroke='red', stroke_width=2))
        
    
    # Fill in shape
    
    
    
    d.savePng('example.png')
    
