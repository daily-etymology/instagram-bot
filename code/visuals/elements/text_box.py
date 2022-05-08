#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper class to handle text flowing logic
"""
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

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

            self.text_rgba = []
            for c, opacity in enumerate(self.opacity):
                self.text_rgba.append([tmp_colour[0],
                                  tmp_colour[1],
                                  tmp_colour[2],
                                  int(self.opacity[c] * 255)])
        
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
            
            while 1:
                tmp_font = ImageFont.truetype(self.font_name, font_size)
                new_shape = self.compute_size(combine_text, tmp_font)
                
                if new_shape[0] > self.width or new_shape[1] > self.height:
                    font_size -= 1
                    tmp_font = ImageFont.truetype(self.font_name, font_size)
                    new_shape = self.compute_size(combine_text, tmp_font) #self.get_text_dimensions(combine_text, tmp_font)
                    self.text_shape = new_shape
                    self.font = tmp_font
                    
                    return font_size
                
                font_size += 1
        else:            
            solutions = []
                   
            print("computing text sizes", self.text_string)
            for font_size in range(1, 80):
                solution = self.greedy_solver_multiline(text_list, font_size)
                
                if solution["valid"]:
                    solutions.append(solution)
                            
        best_score = 2 ** 31 - 1
        best_id = 2 ** 31 - 1
        max_font = -1
        for c, s in enumerate(solutions):
            if s["font_size"] > max_font:
                max_font = s["font_size"]
                best_id = c

        best_solution = solutions[best_id]
        
        font_size = best_solution["font_size"]
        tmp_font = ImageFont.truetype(self.font_name, font_size)
        self.font = tmp_font
        self.text_string = best_solution["full_string"]
        new_shape = self.get_text_dimensions(self.text_string, tmp_font)        
        self.new_shape = best_solution["new_shape"]
        
        return font_size
    
    def greedy_solver_multiline(self, text_list, font_size):
        tmp_font = ImageFont.truetype(self.font_name, font_size)
                
        lines = []
        line_sizes = []
        line = ""
        for c, word in enumerate(text_list):
            # print(word, "-", line)
            new_shape = self.compute_size(line, tmp_font)
            next_shape = [0, 0]
            if c < len(text_list) - 1:
                next_shape = self.compute_size((line + text_list[c + 1]).strip(), tmp_font)
            if next_shape[0] > self.width:
                lines.append(line.strip())
                line_sizes.append(new_shape)
                line = word + " "
            else:
                line += word + " "                
        lines.append(line.strip())
        line_sizes.append(new_shape)
        
        combined_str = ""
        
        for line in lines:
            combined_str += line + "\n"
        combined_str = combined_str.strip()
        
        # Compute score
        height = 0
        widths = []
        for dim in line_sizes:
            height += dim[1]
            widths.append(dim[0])
            
        score = (height - self.height) ** 2
        for width in widths:
            score += (width - self.width) ** 2
            
        final_shape = self.compute_size(combined_str, tmp_font)
        
        valid_sol = True
        if final_shape[0] > self.width or final_shape[1] > self.height:
            valid_sol = False
        
        solution = {}        
        solution["font_size"] = font_size
        solution["score"] = score
        solution["new_shape"] = new_shape
        solution["full_string"] = combined_str
        solution["valid"] = valid_sol
        
        return solution
            
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

            if new_shape[0] > self.width or new_shape[1] > self.height:
                break       
            index += 1
        
        l = [len(i) for i in text_list]
        n = len(l)
        M = len(m_string)
        
        sol = solveWordWrap(l, n, M)
                
        line_solutions = printSolution(sol[0], sol[1])
        row_ids = solution_to_rownumber(line_solutions[1])
                        
        full_string = ""
        prev_row = 0
        
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
        
        score = (new_shape[0] - self.width) ** 2 + (new_shape[1] - self.height) ** 2

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
        tmp_font = ImageFont.truetype(self.font_name, self.font_size)
        self.text_shape = self.compute_size(self.text_string, tmp_font)
        
        if self.text_align == "top":
            x = self.x - self.width
            y = self.y - self.height
        elif self.text_align == "center":
            x = self.x - (self.width + self.text_shape[0]) / 2
            y = self.y - (self.height + self.text_shape[1]) / 2
            
        return x,y


if __name__ == "__main__":
    import numpy as np
    import drawSvg as draw
    
    import os

    from polygon import Polygon
    
    root_path = os.path.abspath(__file__).replace("code/visuals/elements/text_box.py", "")
    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    
    d = draw.Drawing(SCREEN_WIDTH, SCREEN_HEIGHT, origin='center', displayInline=False)
    
    n_sides = 5

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

    d.savePng('example.png')
     
    image = Image.open('example.png')
    
    draw = ImageDraw.Draw(image)
    
    print(box_points_bottom[0], box_points_bottom[1], box_points_bottom[2], box_points_bottom[3])
    
    text_box = TextBox(duration = 5,
                       framerate = 60,
                       x = box_points_bottom[0],
                        y = box_points_bottom[1],
                        width = box_points_bottom[2],
                        height = box_points_bottom[3],
                        text = "By the 19th century we already had arrogant, haughty, and supercilious, but there was apparently need for more because by mid-century the language had garnered two others: toplofty and its variant toploftical. The source of these is likely the phrase top loft, which refers to the highest story of a building.",
                        font_name = root_path + 'fonts/CharisSILI.ttf',
                       
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
                       font_name = root_path + 'fonts/Louis George Cafe/Louis George Cafe Bold.ttf',
                       
                       max_lines = None)  
    
    draw.text(text_box.text_position, text_box.text_string, (255,0,0),
              font = text_box.font
              )
    
    image.save('example.png')
