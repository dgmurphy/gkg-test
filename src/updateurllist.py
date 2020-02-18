
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
from lib.utils import fname_from_url


def load_files_df(df_file):

    try:
        logging.info("Reading " + df_file)
        df = pd.read_table(df_file, sep=' ', usecols=[0,1,2], names=['id', 'checksum', 'url'], header=None)
        
    except Exception as e: 
        logging.critical("Not parsed: " + df_file + "\n" + str(e))
        sys.exit()   

    return df


def build_gkg_urls(master_list):
    
    logging.info("Loading GDELT Master File List")
    gdelt_list_df = load_files_df(master_list)
    logging.info("gdelt_list_df " + str(gdelt_list_df.shape))

    regex = '202002.{9}gkg'
    #regex = '2020021001.{5}gkg'
    logging.info("filtering on " + regex)

    # Grab rows that contain 'gkg' in the url column
    gdelt_list_df = gdelt_list_df[gdelt_list_df['url'].str.contains(
        regex) == True]

    # Save the url column only
    gdelt_list_df = gdelt_list_df['url']
    logging.info("filtered list length: " + str(gdelt_list_df.shape[0]))

    # write the gkg file
    with open(GKG_FILE_LIST, 'w') as f:
        logging.info("writing " + GKG_FILE_LIST)
        gdelt_list_df.to_csv(f, index=False, sep="\t", header=False)



def main():

    ans = ""
    while (ans != 'y') and (ans != 'n'):
        ans = input("Download new GDELT Master File List? [y/n] ")
        ans = ans.lower().strip()

    master_url = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"
    file_name = DATA_DIR + fname_from_url(master_url)

    if ans == 'y':

        logging.info("Downloading master file list.")

        with open(file_name, "wb") as file:
            # get request
            response = get(master_url)
            # write to file
            file.write(response.content)

    else:
        logging.info("Using existing master file list.")

    build_gkg_urls(file_name)


if __name__ == '__main__':
    main()
    print("DONE\n")