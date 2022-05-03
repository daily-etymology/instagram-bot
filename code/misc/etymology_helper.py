#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to load and process the etymology data
"""
import pandas as pd
import numpy as np
import os

class EtymologyHelper():
    def __init__(self):
        filepath = os.path.abspath(__file__).replace("code/misc/etymology_helper.py", "")
        df = pd.read_parquet(filepath + "data/words.parquet")
        new_df = df[df["usage"].isna() == False]

        self.row_id = np.random.randint(0,new_df.shape[0] - 1)
        self.new_row = new_df.iloc[self.row_id]
        
    def get_hastags(self):
        pass
    
if __name__ == "__main__":
    etym = EtymologyHelper()
    print(etym.new_row)
