#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to keep track of all objects used in the post. This includes locations
of the text boxes and other things
"""

class PostLayout():
    def __init__(self, bg_object = None):
        self.compute_inner_box = None
        if not bg_object is None:
            if bg_object.obj_name == "polygon":
                self.compute_inner_box = bg_object.compute_inner_box
        
        self.objects = []
        
        self.gen_first_screen()
        self.gen_second_screen()
        
    def gen_first_screen(self):
        obj_dict = {
            "duration" : 5,
            "start_time" : 0
            }
        if not self.compute_inner_box is None:
            theme = {}
            rect_settings = self.compute_inner_box(250,100)
            obj_dict["object_type"] = "rectangle"
            theme["position"] = rect_settings[:2]
            theme["width"] = rect_settings[2]
            theme["height"] = rect_settings[3]
            obj_dict["theme"] = theme
        
        self.objects.append(obj_dict)
                
        obj_dict = {
            "duration" : 5,
            "start_time" : 0
            }
        if not self.compute_inner_box is None:
            theme = {}
            rect_settings = self.compute_inner_box(-150, 300)
            obj_dict["object_type"] = "rectangle"
            theme["position"] = rect_settings[:2]
            theme["width"] = rect_settings[2]
            theme["height"] = rect_settings[3]
            obj_dict["theme"] = theme
        
        self.objects.append(obj_dict)
        
        
        obj_dict = {
            "duration" : 5,
            "start_time" : 0
            }
        if not self.compute_inner_box is None:
            theme = {}
            rect_settings = self.compute_inner_box(-400, 150)
            obj_dict["object_type"] = "rectangle"
            theme["position"] = rect_settings[:2]
            theme["width"] = rect_settings[2]
            theme["height"] = rect_settings[3]
            obj_dict["theme"] = theme
        
        self.objects.append(obj_dict)
        
    def gen_second_screen(self):
        obj_dict = {
            "duration" : 5,
            "start_time" : 5
            }
        if not self.compute_inner_box is None:
            theme = {}
            rect_settings = self.compute_inner_box(200, 200)
            obj_dict["object_type"] = "rectangle"
            theme["position"] = rect_settings[:2]
            theme["width"] = rect_settings[2]
            theme["height"] = rect_settings[3]
            obj_dict["theme"] = theme
        
        self.objects.append(obj_dict)
                
        obj_dict = {
            "duration" : 5,
            "start_time" : 5
            }
        if not self.compute_inner_box is None:
            theme = {}
            rect_settings = self.compute_inner_box(-300, 400)
            obj_dict["object_type"] = "rectangle"
            theme["position"] = rect_settings[:2]
            theme["width"] = rect_settings[2]
            theme["height"] = rect_settings[3]
            obj_dict["theme"] = theme
        
        self.objects.append(obj_dict)
        
            

