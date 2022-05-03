#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper class to handle text flowing logic
"""
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

import string
import numpy as np

from visuals.helpers.colour_library import hex_to_RGB

from visuals.helpers.text_wrapper import solveWordWrap, solution_to_rownumber, printSolution

class TextBox():
    def __init__(self, 
                 duration, framerate,
                 x, y, width, height,
                 text, font_name, text_align = "top", max_lines = None,
                 theme = {}):
        self.obj_name = "text_box"
        self.duration = duration
        self.framerate = framerate
        
        self.x = abs(x - 500)
        self.y = abs(y - 500)
                
        self.width = width
        self.height = height
        self.text_string = text
        self.font_name = font_name
        
        self.text_align = text_align
        self.max_lines = max_lines
        
        self.text_shape = None
        self.font = None
        
        self.theme = dict(theme)
        
        if self.theme == {}:
            self.font_size = self.greedy_solver()
            self.text_position = self.compute_text_position()
        else:
            # print(theme)
            self.font_size = theme["font_size"]
            self.font = ImageFont.truetype(self.font_name, self.font_size)
            self.text_position = theme["text_position"]
            self.text_string = theme["text_string"]
        
        
            if not "text_colour" in self.theme.keys():
                self.theme["text_colour"] = "#ffaa77"
            if theme["text_colour"] is None:
                self.theme["text_colour"] = "#77aaff"
            
            
            assert "peak_start" in theme.keys(), "peak_start is not specified for textbox"
            self.peak_start = theme["peak_start"]
            
            assert "peak_end" in theme.keys(), "peak_end is not specified for textbox"
            self.peak_end = theme["peak_end"]
            
            assert "opacity_min" in theme.keys(), "opacity_min is not specified for textbox"
            self.opacity_min = theme["opacity_min"]
            
            assert "opacity_max" in theme.keys(), "opacity_max is not specified for textbox"
            self.opacity_max = theme["opacity_max"]
            
            self.colours = np.repeat(self.theme["text_colour"], int(np.ceil(duration*framerate)))
            self.opacity = self.calc_opacity()
            
            # Compute RGBA
            if type(self.theme["text_colour"]) == str:
                tmp_colour = hex_to_RGB(self.theme["text_colour"])
            else:
                tmp_colour = self.theme["text_colour"]
            
            # self.rgba = tmp_colour
            self.text_rgba = []
            for c, opacity in enumerate(self.opacity):
                self.text_rgba.append([tmp_colour[0],
                                  tmp_colour[1],
                                  tmp_colour[2],
                                  int(self.opacity[c] * 255)])
                                  
            # print(self.rgba)
            
        
    def calc_opacity(self):
        start_frame_0 = 0
        start_frame_1 = int(np.ceil(self.duration * self.peak_start * self.framerate))
        
        end_frame_0 = int(np.ceil(self.duration * self.peak_end * self.framerate))
        end_frame_1 = int(np.ceil(self.duration * self.framerate))
        
        duration_fadein = start_frame_1 - start_frame_0 + 1
        duration_fadeout = end_frame_1 - end_frame_0 + 1
        
        duration_inner = (int(self.duration * self.framerate) - 
                        duration_fadein - duration_fadeout)
        
        opacity_fadein = list(np.linspace(self.opacity_min,self.opacity_max,duration_fadein))
        opacity_inner = list(np.repeat(self.opacity_max,duration_inner))
        opacity_fadeout = list(np.linspace(self.opacity_max,self.opacity_min,duration_fadeout))
        
        opacity_total = opacity_fadein
        opacity_total += opacity_inner
        opacity_total += opacity_fadeout
        
        return opacity_total
    
    def greedy_solver(self, debug = False):
        font_size = 1
        
        text_string = self.text_string
        text_list = text_string.split(" ")
        new_line_loc = []
        
        if self.max_lines == 1:
            combine_text = self.text_string
            #print(combine_text)
            
            while 1:
                tmp_font = ImageFont.truetype(self.font_name, font_size)
                new_shape = self.compute_size(combine_text, tmp_font)
                #new_shape = tmp_font.getsize(combine_text)                
                #new_shape = self.get_text_dimensions(combine_text, tmp_font)
                
                if new_shape[0] > self.width or new_shape[1] > self.height:
                    font_size -= 1
                    tmp_font = ImageFont.truetype(self.font_name, font_size)
                    new_shape = self.get_text_dimensions(combine_text, tmp_font)
                    self.text_shape = new_shape
                    self.font = tmp_font
                    
                    return font_size
                
                font_size += 1
        else:            
            solutions = []
                        
            for font_size in range(20, 80):
                solution = self.tex_solver(text_list, text_string, font_size)
                if solution:
                    solutions.append(solution)
                    # font_size +=  1
                # else:
                #     break
            
        best_score = 2 ** 31 - 1
        best_id = 2 ** 31 - 1
        for c, s in enumerate(solutions):
            if s["score"] < best_score:
                best_score = s["score"]
                best_id = c
        # print(solutions)
        best_solution = solutions[best_id]
        
        
        # print(best_solution)
        
        self.font_size = best_solution["font_size"]
        tmp_font = ImageFont.truetype(self.font_name, self.font_size)
        self.font = tmp_font
        self.text_string = best_solution["full_string"]
        new_shape = self.get_text_dimensions(self.text_string, tmp_font)        
        self.new_shape = best_solution["new_shape"]
        
        return font_size
    
    def tex_solver(self, text_list, text_string, font_size):
        combine_text = ""
        solution = {}
        m_string = ""
        
        solution["font_size"] = font_size
        
        index = 0
        # Compute M (maximum number of characters allowed for font_size)
        while 1:
            if index > len(text_string) - 1:
                break
            tmp_font = ImageFont.truetype(self.font_name, font_size)
            
            m_string += text_string[index]
            
            new_shape = self.compute_size(m_string, tmp_font)
            
            # print(new_shape, [self.width, self.height])
            if new_shape[0] > self.width or new_shape[1] > self.height:
                break       
            index += 1
        # print(m_string)
            
        
        # print(f"font_size: {font_size} \t m: {len(m_string)}")
        l = [len(i) for i in text_list]
        n = len(l)
        M = len(m_string)
        
        sol = solveWordWrap(l, n, M)
                
        line_solutions = printSolution(sol[0], sol[1])
        # print(line_solutions[1], M, l)
        row_ids = solution_to_rownumber(line_solutions[1])
                        
        full_string = ""
        prev_row = 0
        
        
        # print(len(row_ids), len(text_list))
        # print(sol)
        # print(row_ids)
        
        for c, row in enumerate(row_ids):
            sep_char = " "
            if c == 0:
                sep_char = ""
            if prev_row != row:
                prev_row = row
                sep_char = "\n"
                
            full_string += sep_char + text_list[c]
        
        self.text_string = full_string
        self.text_shape = new_shape
        self.font = tmp_font
        
        # Compute the textbox size
        new_shape = self.compute_size(full_string, tmp_font)
        # print(full_string)
        # print(row_ids)
        # print(new_shape, [self.width, self.height])
        
        score = (new_shape[0] - self.width) ** 2 + (new_shape[1] - self.height) ** 2
        # print(score)
        
        # solution["score"] = score
        # solution["new_shape"] = new_shape
        # solution["full_string"] = full_string

        # return solution
        
        if new_shape[0] < self.width and new_shape[1] < self.height:
            solution["score"] = score
            solution["new_shape"] = new_shape
            solution["full_string"] = full_string

            return solution
        else:
            return False
            
    def compute_size(self, text_string, font):          
        # Determine text size using a scratch image.
        imgtmp = Image.new("RGBA", (1,1))
        drawtmp = ImageDraw.Draw(imgtmp)
        return drawtmp.textsize(text_string, font)
    
    def get_pil_text_size(text, font):
        size = font.getsize(text)
        return size
    
    def get_text_dimensions(self, text_string, font):
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = font.getmetrics()
    
        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent
    
        return [text_width, text_height]
    
    def compute_text_position(self):       
        if self.text_align == "top":
            x = self.x - self.width
            y = self.y - self.height
        elif self.text_align == "center":
            x = self.x - (self.width + self.text_shape[0]) / 2
            y = self.y - (self.height + self.text_shape[1]) / 2
            
        # print(x,y, self.text_shape, (self.width, self.height), self.font_size)
        return x,y


if __name__ == "__main__":
    import numpy as np
    import drawSvg as draw

    from polygon import Polygon
    
    #dummy_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque elementum sem nec tortor varius, vel molestie tortor consectetur. Morbi eleifend est a nisi molestie maximus. Aliquam condimentum vulputate arcu eget dapibus. Quisque interdum purus eget lacus vestibulum pellentesque. Quisque ultricies eget nunc eget hendrerit. Vestibulum lobortis, orci ac ultricies pharetra, augue odio viverra enim, sed finibus elit nunc eget neque. Fusce at leo pellentesque, dapibus neque pharetra, consequat orci. Sed et nisi arcu. Cras sit amet pharetra ipsum. Aliquam fringilla lectus mattis mi efficitur, eget blandit augue pharetra. Quisque mollis egestas orci quis facilisis. Morbi ullamcorper enim ac elit pharetra bibendum. Donec malesuada mollis leo, ut aliquam dui iaculis mollis. Mauris placerat enim tellus, ut suscipit erat laoreet vitae. In hac habitasse platea dictumst. Etiam nec libero nibh."
    dummy_text = "Test this reasonably long string. Twinkle twinkle little star, how I wonder what you are. Shinning long string. Twinkle twinkle up above so high, like a diamond in the sky. Twinkle twinkle little star, how I wonder what you are. Twinkle twinkle little star, how I wonder what you are. Shinning up above so high, like a diamond in the sky. Twinkle twinkle little star, how I wonder what you are. Twinkle twinkle little star, how I wonder what you are. Shinning up above so high, like a diamond in the sky. Twinkle twinkle little star, how I wonder what you are. Twinkle twinkle little star, how I wonder what you are. Shinning up above so high, like a diamond in the sky. Twinkle twinkle little star, long string. Twinkle twinkle how I wonder what you are. Shinning long string. Twinkle twinkle up above so high, like a diamond in the sky. Twinkle twinkle little star, how I wonder what you are. Twinkle twinkle little star, how I wonder what you are. Shinning up above so high, like a diamond in the sky. Twinkle twinkle little star, how I wonder what you are. Twinkle twinkle little star, how I wonder what you are. Shinning up above so high, like a diamond in the sky. Twinkle twinkle little star, how I wonder what you are. Twinkle twinkle little star, how I wonder what you are. Shinning up above so high, like a diamond in the sky. Twinkle twinkle little star, long string. Twinkle twinkle how I wonder what you are."
    #dummy_text = "This is some random text that has no meaning. I just want to fill in the space with random nonsense which looks somewhat legit."
    #dummy_text = "Hello, how are you?"
    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    
    d = draw.Drawing(SCREEN_WIDTH, SCREEN_HEIGHT, origin='center', displayInline=False)
    
    n_sides = 8

    p = Polygon(n_sides,500, 1, 60, phi =  5*np.pi/(2) )
                   
    
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
        
    offset =  -300
    height =  400
    
    box_points_bottom = p.compute_inner_box(offset, height)
    
    
    d.append(draw.Rectangle(box_points_bottom[0],
                            box_points_bottom[1],
                            box_points_bottom[2],
                            box_points_bottom[3],
                            opacity = 0))
    
    offset =  200
    height =  200
    
    box_points_top = p.compute_inner_box(offset, height)
    
    
    d.append(draw.Rectangle(box_points_top[0],
                            box_points_top[1],
                            box_points_top[2],
                            box_points_top[3],
                            opacity = 0))
        
    # # Draw text
    # d.append(draw.Text('Basic text', 40, -100, 350, 
    #                    fill='blue', font = "fonts/The Californication.ttf"))  # Text with font size 8
    
    d.savePng('example.png')
     
    image = Image.open('example.png')
    
    draw = ImageDraw.Draw(image)
    
    
    text_box = TextBox(duration = 5,
                       framerate = 60,
                       x = box_points_bottom[0],
                        y = box_points_bottom[1],
                        width = box_points_bottom[2],
                        height = box_points_bottom[3],
                        text = "This is some random text that has no meaning. I just want to fill in the space with random nonsense which looks somewhat legit.",
                        #font_name = 'fonts/Spring in May.ttf',
                        #font_name = 'fonts/The Californication.ttf',
                        #font_name = 'fonts/Afterglow-Regular.ttf',
                        #font_name = 'fonts/Hello Valentina.ttf',
                        #font_name = 'fonts/Birds of Paradise.ttf',
                        #font_name = 'fonts/Baby Doll.ttf',
                        font_name = '../fonts/Louis George Cafe/Louis George Cafe.ttf',
                       
                        max_lines = None)  
    
    draw.text(text_box.text_position, text_box.text_string, (255,0,0),
              font = text_box.font
              )
    
    text_box = TextBox(duration = 5,
                       framerate = 60,
                       x = box_points_top[0],
                       y = box_points_top[1],
                       width = box_points_top[2],
                       height = box_points_top[3],
                       text = "\"Hello, how are you?\"",
                       #font_name = 'fonts/Spring in May.ttf',
                       #font_name = 'fonts/The Californication.ttf',
                       #font_name = 'fonts/Afterglow-Regular.ttf',
                       #font_name = 'fonts/Hello Valentina.ttf',
                       #font_name = 'fonts/Birds of Paradise.ttf',
                       #font_name = 'fonts/Baby Doll.ttf',
                       font_name = '../fonts/Louis George Cafe/Louis George Cafe Bold.ttf',
                       
                       max_lines = None)  
    
    draw.text(text_box.text_position, text_box.text_string, (255,0,0),
              font = text_box.font
              )
    
    image.save('example.png')

    
    
