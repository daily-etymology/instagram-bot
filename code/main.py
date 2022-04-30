#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ffmpeg -r 60 -i example%d.png -c:v libx264 -preset veryslow -crf 18 -pix_fmt yuv420p o.mp4 -y
# ffmpeg -i o.mp4 -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 o.gif -y

from pathlib import Path

from display import Display
import drawSvg as draw


if __name__ == "__main__":
    # Create output folder
    Path("frames").mkdir(parents=True, exist_ok=True)
    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
            
    print("generating frames")
    display = Display()
    
    print("exporting frames")
    for c,frame in enumerate(display.frames):
        d = draw.Drawing(SCREEN_WIDTH, SCREEN_HEIGHT, origin='center', displayInline=False)
        
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
        
        d.savePng('frames/example{}.png'.format(c))
        #1/0
        print(f"\rframe:{c + 1} out of {len(display.frames)} \t {100*(c + 1)/len(display.frames):.3f}%", end="")
    print()  # New line