import pandas as pd 
import numpy as np
import os.path
import sys
import time
from lib.logging import logging
import datetime
from lib.constants import *
from lib.utils import *
import glob


def main():

    # create blank full df
    df = pd.DataFrame(columns=GKG_COLUMN_NAMES)

    file_list = glob.glob(ARMY_GKG_DAILY_DIR + "Army_GKG_by_day*.csv")

    for f in file_list:
        
        logging.info("reading" + f)

        # read the file into temp df
        tdf = pd.read_csv(f, header=0, sep='\t', names=GKG_COLUMN_NAMES, 
            index_col=False)

        # append temp df to full df
        df = df.append(tdf, ignore_index=True)


    logging.info("consolidated df shape: " + str(df.shape))

    # build a list of the V1THEMES column
    themes_list = df['V1THEMES'].tolist()
    #print(f"themes list length: " + str(len(themes_list)))
    #print(themes_list[10])


    themes_dict = {}
    for line in themes_list:
        l = line.strip()
        themes = l.split(";")
        for t in themes:
            t = t.strip()
            if len(t) > 1:
                tn = t.split(',')[0]
                if tn in themes_dict:
                    themes_dict[tn] += 1
                else:
                    themes_dict[tn] = 1

    # add the V2 Themes
    
    #print(str(themes_dict))
    themes_hist_df = pd.DataFrame.from_dict(themes_dict, orient='index')
    themes_hist_df = themes_hist_df.sort_values(by=0, ascending=False)

    #print(str(themes_hist_df.head(500)))
    outfile = ARMY_GKG_DAILY_DIR + "ThemesHistogram.csv"
    logging.info("writing " + outfile)
    themes_hist_df.to_csv(outfile, header=False, sep="\t")

if __name__ == '__main__':
    main()
    print("DONE\n")
