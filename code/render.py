#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ffmpeg -r 60 -i example%d.png -c:v libx264 -preset veryslow -crf 18 -pix_fmt yuv420p o.mp4 -y
# ffmpeg -i o.mp4 -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 o.gif -y

from pathlib import Path

from visuals.display import Display
import drawSvg as draw

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import os


def gen_frames(etym_data, SCREEN_WIDTH = 1000, SCREEN_HEIGHT = 1000):
    # Create output folder
    Path("frames").mkdir(parents=True, exist_ok=True)   

    print("generating frames")
    display = Display(etym_data)

    print("exporting frames")
    for c,frame in enumerate(display.frames):
        d = draw.Drawing(SCREEN_WIDTH, SCREEN_HEIGHT, origin='center', displayInline=False)

        text_box_objects = []

        for f in frame:
            if f == {}:
                continue
            if f["object"] == "background":
                d.append(draw.Lines(-SCREEN_WIDTH//2, -SCREEN_HEIGHT//2,
                                    SCREEN_WIDTH//2, -SCREEN_HEIGHT//2,
                                    SCREEN_WIDTH//2, SCREEN_HEIGHT,
                                    -SCREEN_WIDTH//2, SCREEN_HEIGHT,
                                    close=False,
                            fill=f["colour"],
                            stroke='black'))
            if f["object"] == "bubble":
                d.append(draw.Circle(f["position"][0], f["position"][1], f["radius"],
                        fill=f["colour"], stroke_width=0, stroke='black', 
                        fill_opacity=f["opacity"]))

            if f["object"] == "polygon":
                # Add lines
                for i in range(len(f["pivot_points"])):
                    d.append(draw.Lines(0,0,
                        f["pivot_points"][i-1][0],f["pivot_points"][i-1][1],
                        f["pivot_points"][i][0],f["pivot_points"][i][1],
                                        close=False,
                                fill=f["colour"],
                                stroke_width = 2,
                                opacity = f["opacity"],
                                ))
                    # d.append(draw.Line(f["pivot_points"][i-1][0], f["pivot_points"][i-1][1],
                    #                    f["pivot_points"][i][0], f["pivot_points"][i][1],
                    #             stroke='red', stroke_width=2))

            if f["object"] == "rectangle":
                d.append(draw.Rectangle(f["x"],
                                        f["y"],
                                        f["width"],
                                        f["height"],
                                        fill = f["colour"],
                                        opacity = f["opacity"]
                                        ))

            if f["object"] == "text_box":
                text_box_objects.append(f)
                pass

        output_pic_name = 'frames/example{}.png'.format(c)
        d.savePng(output_pic_name)

        if len(text_box_objects) > 0:
            image = Image.open(output_pic_name).convert("RGBA")
            txt = Image.new('RGBA', image.size, (255,255,255,0))

            pil_draw = ImageDraw.Draw(txt)

            for text_object in text_box_objects:
                # print(text_object["text_string"], text_object["text_rgba"])
                font = ImageFont.truetype(text_object["font_name"],
                                          text_object["font_size"])
                pil_draw.text(text_object["text_position"],
                          text_object["text_string"],
                          fill = tuple(text_object["text_rgba"]),
                          font = font
                           )

                image = Image.alpha_composite(image, txt)

            image.save(output_pic_name)
            image.close()

        # 1/0

        print(f"\rframe:{c + 1} out of {len(display.frames)} \t {100*(c + 1)/len(display.frames):.3f}%", end="")
    print()  # New line
    
def render_ffmpeg():
    filepath = os.path.abspath(__file__).replace("code/render.py", "")
    frames_path = filepath + "code/frames/example%d.png"
    out_path = filepath + "code/frames/o.mp4"
    
    cmd = f"ffmpeg -r 60 -i {frames_path} -c:v libx264 -preset veryslow -crf 18 -pix_fmt yuv420p {out_path} -y"
    
    os.system(cmd)

if __name__ == "__main__":
    render_ffmpeg()