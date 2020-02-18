import pandas as pd 
import numpy as np
import os.path
import sys
import time
from requests import get  
import io
from lib.logging import logging
import datetime
from lib.constants import *
from lib.utils import *


def process_zip_file():

    csv = DATA_DIR + '20200215224500.gkg.csv'

    logging.info("Reading " + csv)
    df = pd.read_csv(csv, header=0, sep='\t', names=GKG_COLUMN_NAMES, 
        encoding= 'unicode_escape')
    logging.info("gkg df shape " + str(df.shape))

    # append relevant gkg lines to army df
    # Grab rows that contain 'army' in the url column
    # fdf = df[(df['V1ORGANIZATIONS'].str.contains(ARMY_REGEX, case=False) == True) |
    #                   (df['V2ENHANCEDORGANIZATIONS'].str.contains(
    #                       ARMY_REGEX, case=False) == True)
    #         ]

    # logging.info("fdf shape " + str(fdf.shape))
    #print(str(fdf.head()))

    # update the processed files list
    # with open(FILES_PROCESSED_LIST, "a") as f:
    #     f.write(zip_file_url + "\n")

    # delete the zip file
    # if os.path.exists(zip_file):
    #     logging.info("removing " + zip_file)
    #     os.remove(zip_file)
    # else:
    #     logging.info(zip_file + " missing.")

    print(df.head())

     

    
    
def main():
    process_zip_file()

    

if __name__ == '__main__':
    main()
    print("DONE\n")
