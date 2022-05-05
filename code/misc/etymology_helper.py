#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to load and process the etymology data
"""
import pandas as pd
import numpy as np
import os
import datetime
import string
import requests
import re

class EtymologyHelper():
    def __init__(self):
        filepath = os.path.abspath(__file__).replace("code/misc/etymology_helper.py", "")
        df = pd.read_parquet(filepath + "data/words.parquet")
        
        self.new_df = df[df["usage"].isna() == False]
        
        self.hashtags = self.get_hastags()

        self.row_id = np.random.randint(0, self.new_df.shape[0] - 1)
        self.new_row = self.new_df.iloc[self.row_id]
        
        self.caption = self.gen_caption()
        
    def get_hastags(self):
        fallback_hashtags = ["#etymology",
                             "#wordoftheday",
                             "#english",
                             "#words", "#word",
                             "#language", "#vocabulary", "#etymologygram",
                             "#dictionary", "#learnenglish", "#love", "#definition",
                             "#wordgram", "#wordfortheday", "#latin", "#obscurewords",
                             "#unknownwords", "#linguistics", "#englishvocabulary",
                             "#newwords", "#newword", "#real", "#art", "#follow",
                             "#instagood", "#instadaily", "#photooftheday",
                             "#learning", "#indigenous", "#englishlanguage"]
        
        # Try to get latest most popular hashtags for etymology
        try:
            r = requests.get("http://best-hashtags.com/hashtag/etymology/")
            html = r.text
            hashtags = re.findall('are\s(.*?)\"', html)[0].strip().split(" ")
        except:
            print("failed to obtain new hashtags :(")
            hashtags = fallback_hashtags
        
        return hashtags
    def gen_message(self):
        pass
    
    def gen_caption(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        
        word_type_article = "an"
        if self.new_row["word_type"] in ["verb", "noun"]:
            word_type_article = "a"
        
        caption_string = """Word: \t {0} is {1} {2}.
Example sentence: \t {3}
Meaning: \t {4}
Etymology: \t {5}

Source: \t {6}
{7}
{8}
""".format(string.capwords(self.new_row["word"]),
word_type_article,
self.new_row["word_type"],
self.new_row["usage"],
self.new_row["def"],
self.new_row["etym"],
self.new_row["url"],
" ".join(self.hashtags),
date_str
)
        
        return caption_string
    
    def get_row(self):
        for i in range(self.new_df.shape[0]):
            yield self.new_df.iloc[i]
    
if __name__ == "__main__":
    etym = EtymologyHelper()
    # print(etym.new_row)
    # print(etym.gen_caption())
