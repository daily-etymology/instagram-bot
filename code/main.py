#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from render import gen_frames, render_ffmpeg
from misc.etymology_helper import EtymologyHelper

if __name__ == "__main__":
    # Get etymology data
    etym = EtymologyHelper()
    etym_row = etym.new_row
    
    #gen_frames(etym_row)
    #render_ffmpeg()