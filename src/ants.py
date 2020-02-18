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


def download(url):

    logging.info("Downloading " + url)
    file_name = fname_from_url(url)

    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


def build_url_queue(use_failed_files):

    if use_failed_files:
        input_file_list = FAILED_FILES_LIST
    else:
        input_file_list = GKG_FILE_LIST
    
    # Read the gkg file list
    gkg_list = []
    try:
        with open( input_file_list ) as f :
            gkg_list = f.read().splitlines() 
            
    except EnvironmentError: 
        logging.info(input_file_list + " not read")

    # Read the processed files list if it exists
    logging.info("reading processed files list")
    processed_files = []
    try:
        with open( FILES_PROCESSED_LIST ) as f :
            processed_files = f.read().splitlines()
            f.close()

    except EnvironmentError: 
            logging.info("processed files list not read")
            
    logging.info("processed files length: " + str(len(processed_files)))

    # Build the queue by comparing the processed files list with the gkg list
    files_queue = []
    for url in gkg_list:
        if url not in processed_files:
            files_queue.append(url)

        
    # delete the failed files list
    if os.path.exists(FAILED_FILES_LIST):
        os.remove(FAILED_FILES_LIST)


    return files_queue


def process_zip_file(zip_file_url):

    zip_file = fname_from_url(zip_file_url)

    try:
        logging.info("Reading " + zip_file)

        #requires unicode escape for some files
        df = pd.read_csv(zip_file, compression='zip', header=0, 
                sep='\t', names=GKG_COLUMN_NAMES, encoding= 'unicode_escape')

        logging.info("gkg df shape " + str(df.shape))

        # append relevant gkg lines to army df
        # Grab rows that contain 'army' in the url column
        fdf = df[(df['V1ORGANIZATIONS'].str.contains(ARMY_REGEX, case=False) == True) |
                          (df['V2ENHANCEDORGANIZATIONS'].str.contains(
                              ARMY_REGEX, case=False) == True)
                ]

        logging.info("fdf shape " + str(fdf.shape))
        #print(str(fdf.head()))
       
        # update the processed files list
        with open(FILES_PROCESSED_LIST, "a") as f:
            f.write(zip_file_url + "\n")

        # delete the zip file
        if os.path.exists(zip_file):
            logging.info("removing " + zip_file)
            os.remove(zip_file)
        else:
            logging.info(zip_file + " missing.")

    except Exception as e:
        logging.error("Problem reading " + zip_file)

    return fdf


def main():

    USE_FAILED_FILES_LIST = False


    startTime = pd.Timestamp('now')
    logging.info("ANTS run started at " + str(startTime))

    # elapsed time working on the current output file
    fileTime = pd.Timestamp('now')

    # add time to output file to prevent overwrites
    timestr = time.strftime("%Y%m%d-%H%M%S")
    outfile = OUTPUT_FILE_PRE + timestr + ".csv"


    # Build the input queue
    files_queue = build_url_queue(USE_FAILED_FILES_LIST)

    if len(files_queue) > 0:
        logging.info(str(len(files_queue)) + " files in queue")
    else:
        logging.info("NO UNPROCESSED FILES IN QUEUE")


    files_processed = 0
    army_gkg_events = 0
    skipped_files = 0
    for zip_file_url in files_queue:

        # Download a file from the queue
        try:
            # UNCOMMENT
            download(zip_file_url)
            
            fdf = process_zip_file(zip_file_url)

            army_gkg_events += fdf.shape[0]

            # create a new file after an hour
            elapsed_time = pd.Timestamp('now') - fileTime
            if  elapsed_time.seconds > 3600:
                timestr = time.strftime("%Y%m%d-%H%M%S")
                outfile = OUTPUT_FILE_PRE + timestr + ".csv"
                fileTime = pd.Timestamp('now')


            fdf.to_csv(outfile, mode='a', header=False, sep='\t', na_rep=' ', index=False)
            logging.info("Wrote results to " + outfile)

            files_processed += 1
            logging.info(f'Completed {files_processed} files')
            logging.info("ARMY GKG EVENTS SO FAR: " + str(army_gkg_events))
            
        
        except Exception as e:

            logging.error("Problem processing " + zip_file_url)

            skipped_files += 1

            with open(FAILED_FILES_LIST, "a") as failedfile:
                failedfile.write(zip_file_url + "\n")

            # delete the zip file
            badfile = fname_from_url(zip_file_url)
            if os.path.exists(badfile):
                os.remove(badfile)

    endTime = pd.Timestamp('now')
    logging.info("ANTS run finished at " + str(endTime))
    logging.info("Elapsed time: " + str(endTime - startTime))        
    logging.info(f"Processed {files_processed} files.")
    logging.info(f"Skipped {skipped_files} files.")
    logging.info(f"Found {army_gkg_events} relevant gkg events")


if __name__ == '__main__':
    main()
    print("DONE\n")
