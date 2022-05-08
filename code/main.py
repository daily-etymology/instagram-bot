#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from render import gen_frames, render_ffmpeg
from misc.etymology_helper import EtymologyHelper
from send_post import make_selenium_insta_post

if __name__ == "__main__":
    # Get etymology data
    etym = EtymologyHelper()
    etym_row = etym.new_row
    
    # Render animation
    gen_frames(etym_row)
    render_ffmpeg()
    
    # Upload to instagram with selenium
    filepath = os.path.abspath(__file__).replace("code/main.py", "")
    output_video_path = filepath + "code/frames/o.mp4"
    
    make_selenium_insta_post(output_video_path, etym.caption)
    
    output_video_path