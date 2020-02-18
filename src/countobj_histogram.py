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
    items_list = df['V1COUNTS'].tolist()
    #print(f"themes list length: " + str(len(themes_list)))
    #print(themes_list[10])


    items_dict = {}
    for line in items_list:   # line has the content from the GKG cell
        l = line.strip()
        items = l.split(";")    # list of top level entities
        for i in items:
            i = i.strip()
            if len(i) > 1:
                ii = i.split('#')[2]     # subfield of entity
                if len(ii) > 1:
                    if ii in items_dict:
                        items_dict[ii] += 1
                    else:
                        items_dict[ii] = 1

    # add the V2 Themes
    
    #print(str(themes_dict))
    items_hist_df = pd.DataFrame.from_dict(items_dict, orient='index')
    items_hist_df = items_hist_df.sort_values(by=0, ascending=False)

    #print(str(themes_hist_df.head(500)))
    outfile = ARMY_GKG_DAILY_DIR + "CountObjectsHistogram.csv"
    logging.info("writing " + outfile)
    items_hist_df.to_csv(outfile, header=False, sep="\t")

if __name__ == '__main__':
    main()
    print("DONE\n")
