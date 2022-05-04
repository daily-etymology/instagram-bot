#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check produced layouts from the render, based on the data
"""
from misc.etymology_helper import EtymologyHelper
from visuals.elements.text_box import TextBox

from PIL import Image
from PIL import ImageDraw

import numpy as np
import drawSvg

import os

from visuals.elements.polygon import Polygon

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
n_sides = 5

def draw_2nd_frame(top_text, botom_text, filename):
    root_path = os.path.abspath(__file__).replace("code/tests/test_etymology_render.py", "")

    d = drawSvg.Drawing(SCREEN_WIDTH, SCREEN_HEIGHT, origin='center', displayInline=False)
    p = Polygon(n_sides,500, 1, 60, phi =  5*np.pi/(2) )

    # Add lines
    for i in range(len(p.pivot_points)):
        d.append(drawSvg.Lines(0,0,
            p.pivot_points[i-1][0],p.pivot_points[i-1][1],
            p.pivot_points[i][0],p.pivot_points[i][1],
                            close=False,
                    fill='#eeee00',
                    stroke_width = 2,
                    opacity = 0.5,
                    ))
        d.append(drawSvg.Line(p.pivot_points[i-1][0], p.pivot_points[i-1][1],
                           p.pivot_points[i][0], p.pivot_points[i][1],
                    stroke='red', stroke_width=2))

    offset =  -300
    height =  400

    box_points_bottom = p.compute_inner_box(offset, height)

    d.append(drawSvg.Rectangle(box_points_bottom[0],
                            box_points_bottom[1],
                            box_points_bottom[2],
                            box_points_bottom[3],
                            opacity = 0.0))

    offset =  200
    height =  200

    box_points_top = p.compute_inner_box(offset, height)

    d.append(drawSvg.Rectangle(box_points_top[0],
                            box_points_top[1],
                            box_points_top[2],
                            box_points_top[3],
                            opacity = 0.0))

    d.savePng(filename)

    image = Image.open(filename)

    draw = ImageDraw.Draw(image)

    text_box = TextBox(duration = 5,
                       framerate = 60,
                       x = box_points_top[0],
                       y = box_points_top[1],
                       width = box_points_top[2],
                       height = box_points_top[3],
                       text = top_text,
                       font_name = root_path + 'fonts/CharisSILI.ttf',
                       text_align = "center",
                       max_lines = None)
    draw.text(text_box.text_position, text_box.text_string, (255,0,0),
              font = text_box.font
              )

    text_box = TextBox(duration = 5,
                       framerate = 60,
                       x = box_points_bottom[0],
                        y = box_points_bottom[1],
                        width = box_points_bottom[2],
                        height = box_points_bottom[3],
                        text = botom_text,
                        font_name = root_path + 'fonts/CharisSILI.ttf',
                        text_align = "top",
                        max_lines = None)
    draw.text(text_box.text_position, text_box.text_string, (255,0,0),
              font = text_box.font
              )

    image.save(filename)

if __name__ == "__main__":
    etym = EtymologyHelper()
    
    c = 1
    for row in etym.get_row():
        if c > 135:
            draw_2nd_frame(row["usage"], row["etym"], "test_{}.png".format(c))
        c += 1


    
    

