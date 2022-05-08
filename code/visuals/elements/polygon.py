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
    
    def compute_inner_box(self, dist_from_origin, height):
        width = self.radius * 2
        
        y_top = max(self.center[0] + dist_from_origin + height, self.center[0] + dist_from_origin)
        y_bottom = min(self.center[0] + dist_from_origin + height, self.center[0] + dist_from_origin)
        
        top_start = [0, y_top]
        top_end = [width, y_top]
        
        bottom_start = [0, y_bottom]
        bottom_end = [width, y_bottom]
        
        box_coordinates = []
        
        top_coordinates = []
        bottom_coordinates = []
        for i in range(len(self.pivot_points)):
            l1_start = self.pivot_points[i-1]
            l1_end = self.pivot_points[i]
            coordinate_top = self.lines_intersect(l1_start, l1_end, top_start, top_end)
            coordinate_bottom = self.lines_intersect(l1_start, l1_end, bottom_start, bottom_end)
            
            if coordinate_top:
                box_coordinates.append(coordinate_top)
                top_coordinates.append(coordinate_top)
                
            if coordinate_bottom:
                box_coordinates.append(coordinate_bottom)
                bottom_coordinates.append(coordinate_bottom)
        
        x_top_list = []        
        for x in top_coordinates:
            x_top_list.append(x[0])    
        x_top_left = min(x_top_list)
        x_top_right = max(x_top_list)
        
        x_bottom_list = []
        for x in bottom_coordinates:
            x_bottom_list.append(x[0])    
        x_bottom_left = min(x_bottom_list)
        x_bottom_right = max(x_bottom_list)
       
        # Compute inner points
        x_left, x_right = max(x_top_left, x_bottom_left), min(x_top_right, x_bottom_right)
        
        x, y, width, height = x_left, y_bottom, abs(x_left - x_right), height
        return x, y, width, height
        
    def lines_intersect(self, l1_start, l1_end, l2_start, l2_end):  
        m2 = (l2_start[1] - l2_end[1]) / (l2_start[0] - l2_end[0])
        c2 = l2_start[1] - m2 * l2_start[0]
        
        # Compute y = mx + c coeficients for two lines
        if abs(l1_start[0] - l1_end[0]) < 10**-12:
            y_ = m2 * l1_start[0] + c2
            
            if min(l1_start[1],l1_end[1]) <= y_ <= max(l1_start[1],l1_end[1]):
                return l1_start[0], y_
            return False
                
        m1 = (l1_start[1] - l1_end[1]) / (l1_start[0] - l1_end[0])
        c1 = l1_start[1] - m1 * l1_start[0]
        
        if m1 == m2:
            return False     
                        
        # Check if two lines intersect
        x_ = (c2 - c1) / (m1 - m2)
        y_ = m2 * (c2 - c1) / (m1 - m2) + c2
        
        x_box = [min(l1_start[0], l1_end[0]), max(l1_start[0], l1_end[0])]
        
        y1 = m1 * x_ + c1 
        y2 = m2 * x_ + c2
                                
        if abs(y1 - y2) > 10 ** -12:
            return False
        
                
        if min(x_box) - 10**-9 <= x_ <= max(x_box) + 10**-9:
            return [x_, y_]
        
        return False
        

if __name__ == "__main__":
    n_sides = 18
    # 4 : pi/2
    # 5 : 3 * pi / 2
    p = Polygon(n_sides,500, 1, 60, phi =  5*np.pi/(2) )
    # print(p.pivot_points)
    
    
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
        
    box_points = p.compute_inner_box(-400, 150)
    d.append(draw.Rectangle(box_points[0],box_points[1], box_points[2], box_points[3]))
    
    print(box_points)
    
    # box_points = p.compute_inner_box(300,10)
    # d.append(draw.Rectangle(box_points[0],box_points[1], box_points[2], box_points[3]))
    
    # box_points = p.compute_inner_box(-100,200)
    # d.append(draw.Rectangle(box_points[0],box_points[1], box_points[2], box_points[3]))
    
    # Fill in shape
    #print(p.lines_intersect([5,7],[10,1], [1,10], [15,11]))
    print()
    
    # print(p.lines_intersect(p.pivot_points[1], p.pivot_points[2], [0,-400], [1000,-400]))
    
    d.savePng('example.png')
    
