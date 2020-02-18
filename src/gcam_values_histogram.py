import pandas as pd 
import numpy as np
import os.path
import sys
import time
import string
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

    # build a list of the column
    items_list = df['V2GCAM'].tolist()
    
    # Read CodeBook into dictionary
    with open(GCAM_CODEBOOK, errors="backslashreplace") as f:
        gcam_lines = f.read().splitlines()   

    # Build gcam dictionary
    logging.info("building GCAM dictionary")
    gcam_dict = {}
    skip = True  # skip line 1
    for line in gcam_lines:
        if skip:
            skip = False
        else:
            line = line.strip()
            cols = line.split("\t")
            gcam_dict[cols[0]] = cols[6]
            

    items_dict = {}  # This will hold the pairs => gcam_code : total_score

    logging.info("building histogram")
    for line in items_list:   # line has the content from the GKG cell
        l = line.strip()

        entries = l.split(",")
        for entry in entries:
            entry = entry.strip()
            code = entry.split(":")[0]
            score = entry.split(":")[1]

            if code[0] == "v":
                if code in items_dict:
                    items_dict[code] += float(score)
                else:
                    items_dict[code] = float(score)

    # annotate the gcam codes with their human dimension names
    labeled_items_dict = {}
    logging.info("adding dimension labels")
    for key, value in items_dict.items():
        label = gcam_dict[key]
        labeled_items_dict[key + " " + label] = value
    
    
    #print(str(themes_dict))
    logging.info("building dataframe")
    items_hist_df = pd.DataFrame.from_dict(labeled_items_dict, orient='index')
    items_hist_df = items_hist_df.sort_values(by=0, ascending=False)

    #print(str(themes_hist_df.head(500)))
    outfile = ARMY_GKG_DAILY_DIR + "GCAM_Values_Histogram.csv"
    logging.info("writing " + outfile)
    items_hist_df.to_csv(outfile, header=False, sep="\t")

if __name__ == '__main__':
    main()
    print("DONE\n")
