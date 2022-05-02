#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to load and process the etymology data
"""
import pandas as pd
import numpy as np

class EtymologyHelper():
    def __init__(self):
        df = pd.read_parquet("../data/words.parquet")
        new_df = df[df["usage"].isna() == False]

        self.row_id = np.random.randint(0,new_df.shape[0] - 1)
        self.new_row = new_df.iloc[self.row_id]
        
    def get_hastags(self):
        pass
    
if __name__ == "__main__":
    etym = EtymologyHelper()
    print(etym.new_row)
