#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to keep track of all objects used in the post. This includes locations
of the text boxes and other things
"""
from visuals.helpers.colour_library import invert_colour
from visuals.elements.text_box import TextBox
import os

class PostLayout():
    def __init__(self, etym_data, bg_object = None, theme = {}):
        self.etym_data = etym_data
        self.compute_inner_box = None
        if not bg_object is None:
            if bg_object.obj_name == "polygon":
                self.compute_inner_box = bg_object.compute_inner_box
        
        self.theme = theme
        
        if self.theme["textbox"]["box_colour"] is None:
            self.theme["textbox"]["box_colour"] = self.theme["background"]["colour"]
        
        if self.theme["textbox"]["text_colour"] is None:
            self.theme["textbox"]["text_colour"] = invert_colour(self.theme["background"]["colour"], is_hex = False)
        
        self.objects = []
                
        self.root_path = os.path.abspath(__file__).replace("code/visuals/post_layout.py", "")
        
        self.gen_first_screen()
        self.gen_second_screen()
        
    def gen_first_screen(self):
        obj_dict = {
            "duration" : 5,
            "start_time" : 0
            }
        if not self.compute_inner_box is None:
            theme = dict(self.theme["textbox"])
            rect_settings = self.compute_inner_box(250,100)
            obj_dict["object_type"] = "rectangle"
            theme["position"] = rect_settings[:2]
            theme["width"] = rect_settings[2]
            theme["height"] = rect_settings[3]
            obj_dict["theme"] = dict(theme)
            
            
            self.objects.append(obj_dict)
            
            # Add text box...
            text_box = TextBox( duration = obj_dict["duration"],
                                framerate = 60,
                                x = rect_settings[0],
                                y = rect_settings[1],
                                width = rect_settings[2],
                                height = rect_settings[3],
                                text = self.etym_data["phonetics"],
                                font_name = self.root_path + 'fonts/CharisSILI.ttf',
                                text_align = "center",
                                max_lines = 1)
            
            obj_dict = {
                "duration" : 5,
                "start_time" : 0
                }
            theme = dict(self.theme["textbox"])
            obj_dict["object_type"] = "text_box"
            theme["text_position"] = text_box.text_position
            theme["font_size"] = text_box.font_size
            theme["text_string"] = text_box.text_string
            theme["x"] = text_box.x
            theme["y"] = text_box.y
            theme["width"] = text_box.width
            theme["height"] = text_box.height
            theme["font_name"] = text_box.font_name
            theme["max_lines"] = text_box.max_lines
            theme["text_align"] = text_box.text_align
            
            obj_dict["theme"] = dict(theme)
                        
            self.objects.append(obj_dict)
                                    
        
        if not self.compute_inner_box is None:
            obj_dict = {
                "duration" : 5,
                "start_time" : 5
                }
            theme = dict(self.theme["textbox"])
            rect_settings = self.compute_inner_box(-125, 300)
            obj_dict["object_type"] = "rectangle"
            theme["position"] = rect_settings[:2]
            theme["width"] = rect_settings[2]
            theme["height"] = rect_settings[3]
            obj_dict["theme"] = dict(theme)
            
            
            self.objects.append(obj_dict)
            
            # Add text box...
            text_box = TextBox( duration = obj_dict["duration"],
                                framerate = 60,
                                x = rect_settings[0],
                                y = rect_settings[1],
                                width = rect_settings[2],
                                height = rect_settings[3],
                                text = self.etym_data["word"],
                                font_name = self.root_path + 'fonts/CharisSILI.ttf',
                                text_align = "center",
                                max_lines = 1)
            
            obj_dict = {
                "duration" : 5,
                "start_time" : 0
                }
            theme = dict(self.theme["textbox"])
            obj_dict["object_type"] = "text_box"
            theme["text_position"] = text_box.text_position
            theme["font_size"] = text_box.font_size
            theme["text_string"] = text_box.text_string
            theme["x"] = text_box.x
            theme["y"] = text_box.y
            theme["width"] = text_box.width
            theme["height"] = text_box.height
            theme["font_name"] = text_box.font_name
            theme["max_lines"] = text_box.max_lines
            theme["text_align"] = text_box.text_align
            
            obj_dict["theme"] = dict(theme)
                        
            self.objects.append(obj_dict)
        
            
        obj_dict = {
            "duration" : 5,
            "start_time" : 0
            }
        if not self.compute_inner_box is None:
            theme = dict(self.theme["textbox"])
            rect_settings = self.compute_inner_box(-400, 150)
            obj_dict["object_type"] = "rectangle"
            theme["position"] = rect_settings[:2]
            theme["width"] = rect_settings[2]
            theme["height"] = rect_settings[3]
            obj_dict["theme"] = theme
        
            self.objects.append(obj_dict)
            
            # Add text box...
            text_box = TextBox( duration = obj_dict["duration"],
                                framerate = 60,
                                x = rect_settings[0],
                                y = rect_settings[1],
                                width = rect_settings[2],
                                height = rect_settings[3],
                                text = self.etym_data["word_type"],
                                font_name = self.root_path + 'fonts/CharisSILI.ttf',
                                text_align = "center",
                                max_lines = 1)
            
            obj_dict = {
                "duration" : 5,
                "start_time" : 0
                }
            theme = dict(self.theme["textbox"])
            obj_dict["object_type"] = "text_box"
            theme["text_position"] = text_box.text_position
            theme["font_size"] = text_box.font_size
            theme["text_string"] = text_box.text_string
            theme["x"] = text_box.x
            theme["y"] = text_box.y
            theme["width"] = text_box.width
            theme["height"] = text_box.height
            theme["font_name"] = text_box.font_name
            theme["max_lines"] = text_box.max_lines
            theme["text_align"] = text_box.text_align
            
            obj_dict["theme"] = dict(theme)
                        
            self.objects.append(obj_dict)
        
    def gen_second_screen(self):
        obj_dict = {
            "duration" : 5,
            "start_time" : 5
            }
        if not self.compute_inner_box is None:
            theme = dict(self.theme["textbox"])
            rect_settings = self.compute_inner_box(200, 200)
            obj_dict["object_type"] = "rectangle"
            theme["position"] = rect_settings[:2]
            theme["width"] = rect_settings[2]
            theme["height"] = rect_settings[3]
            obj_dict["theme"] = theme
        
            self.objects.append(obj_dict)
            
            
            # Add text box...
            text_box = TextBox( duration = obj_dict["duration"],
                                framerate = 60,
                                x = rect_settings[0],
                                y = rect_settings[1],
                                width = rect_settings[2],
                                height = rect_settings[3],
                                text = self.etym_data["usage"],
                                font_name = self.root_path + 'fonts/CharisSILI.ttf',
                                text_align = "center",
                                max_lines = None)
            
            obj_dict = {
                "duration" : 5,
                "start_time" : 5
                }
            theme = dict(self.theme["textbox"])
            obj_dict["object_type"] = "text_box"
            theme["text_position"] = text_box.text_position
            theme["font_size"] = text_box.font_size
            theme["text_string"] = text_box.text_string
            theme["x"] = text_box.x
            theme["y"] = text_box.y
            theme["width"] = text_box.width
            theme["height"] = text_box.height
            theme["font_name"] = text_box.font_name
            theme["max_lines"] = text_box.max_lines
            theme["text_align"] = text_box.text_align
            
            obj_dict["theme"] = dict(theme)
                        
            self.objects.append(obj_dict)
                
        
        obj_dict = {
            "duration" : 5,
            "start_time" : 5
            }
        if not self.compute_inner_box is None:
            theme = dict(self.theme["textbox"])
            rect_settings = self.compute_inner_box(-300, 400)
            obj_dict["object_type"] = "rectangle"
            theme["position"] = rect_settings[:2]
            theme["width"] = rect_settings[2]
            theme["height"] = rect_settings[3]
            obj_dict["theme"] = theme
                    
        self.objects.append(obj_dict)
        
        # Add text box...
        text_box = TextBox( duration = obj_dict["duration"],
                            framerate = 60,
                            x = rect_settings[0],
                            y = rect_settings[1],
                            width = rect_settings[2],
                            height = rect_settings[3],
                            text = self.etym_data["def"] + " " +  
                                            self.etym_data["etym"],
                            font_name = self.root_path + 'fonts/CharisSILI.ttf',
                            text_align = "center",
                            max_lines = None)
        
        # print(self.etymology.new_row["etym"])
        obj_dict = {
            "duration" : 5,
            "start_time" : 5
            }
        # print(text_box.font_size, text_box.text_string)
        theme = dict(self.theme["textbox"])
        obj_dict["object_type"] = "text_box"
        theme["text_position"] = text_box.text_position
        theme["font_size"] = text_box.font_size
        theme["text_string"] = text_box.text_string
        theme["x"] = text_box.x
        theme["y"] = text_box.y
        theme["width"] = text_box.width
        theme["height"] = text_box.height
        theme["font_name"] = text_box.font_name
        theme["max_lines"] = text_box.max_lines
        theme["text_align"] = text_box.text_align
        
        # print(theme)
        
        obj_dict["theme"] = dict(theme)
                    
        self.objects.append(obj_dict)
        
            

