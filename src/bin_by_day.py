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



def make_date(row):

    datestr = str(row['V2.1DATE'])
    year = datestr[:4]
    month = datestr[4:6]
    day = datestr[6:8]
    year_month_day = year + "-" + month + "-" + day

    return year_month_day

def main():

    file_list = glob.glob(DATA_DIR + "army_gkg*.csv")

    # create blank full df
    df = pd.DataFrame(columns=GKG_COLUMN_NAMES)

    for f in file_list:
        print(f)

        # read the file into temp df
        tdf = pd.read_csv(f, header=0, sep='\t', names=GKG_COLUMN_NAMES)

        tdf['V2.1DATE'] = tdf['V2.1DATE'].astype(str)

        # append temp df to full df
        df = df.append(tdf, ignore_index=True)

    

    # create a datetime column on the full df
    df['ymd'] = df.apply (lambda row: make_date(row), axis=1)
    df['Datetime'] = pd.to_datetime(df['ymd'], format='%Y-%m-%d')
    #df = df.set_index(pd.DatetimeIndex(df['Datetime']), drop=True)
    df = df.drop(['ymd'], axis=1)

    #print(df.head(500))

    # group full df by day
    daygroups = df.groupby(['Datetime'])
    logging.info("Groups: " + (str(daygroups.describe())))

    # for each group write the output file (do not write the date or the index)
    for name, group in daygroups:
        tname = str(name)
        out_fname = "Army_GKG_by_day_" + tname[:10] + ".csv"
        logging.info("Writing group to " + out_fname)
        group.to_csv(out_fname, index=False, header=False, sep="\t")
        


if __name__ == '__main__':
    main()
    print("DONE\n")
