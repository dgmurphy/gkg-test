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
from itertools import combinations
from collections import Counter
import csv


def make_persons_set(persons_line):

    persons_set = set()
    l = persons_line.strip()
    person_list = l.split(";")
    
    for person in person_list:
        person = person.strip()
        if len(person) > 1:
            persons_set.add(person)

    pairs = []
    pset_tuples = list(combinations(persons_set, 2))
    for tup in pset_tuples:
        pair = sorted(tup)
        pairs.append(pair)

    return pairs


def main():

    # create blank full df
    df = pd.DataFrame(columns=GKG_COLUMN_NAMES)

    file_list = glob.glob(ARMY_GKG_DAILY_DIR + "Army_GKG_by_day*.csv")
    #file_list = glob.glob(ARMY_GKG_DAILY_DIR + "Army_GKG_by_day_2020-02-16.csv")

    for f in file_list:
        
        logging.info("reading" + f)

        # read the file into temp df
        tdf = pd.read_csv(f, header=0, sep='\t', names=GKG_COLUMN_NAMES, 
            index_col=False)

        # append temp df to full df
        df = df.append(tdf, ignore_index=True)


    logging.info("consolidated df shape: " + str(df.shape))


        # DEBUG
    # persons_rows = []
    # persons_rows.append("n1; n2; n3; n4")
    # persons_rows.append("n1; n3; n5; n6")
    gkg_data = [
        ['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 
         'col10', 'col11', 'n1; n2; n3; n4', 'col13', 'col14', 'col15', 'col16', 'col17', 'col18', 
         'col19', 'col20', 'col21', 'col22', 'col23', 'col24', 'col25', 'col26', 'col27'],
        ['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 
         'col10', 'col11', 'n1; n3; n5; n6', 'col13', 'col14', 'col15', 'col16', 'col17', 'col18', 
         'col19', 'col20', 'col21', 'col22', 'col23', 'col24', 'col25', 'col26', 'col27'],         
    ]

    # create blank full df
    #df = pd.DataFrame(gkg_data, columns=GKG_COLUMN_NAMES)

    # make persons column into set
    df['V1PERSONS'] = df.apply(lambda row: make_persons_set(row.V1PERSONS), axis=1)

    # pdf = df[['V1PERSONS']].copy()
    # print(pdf.head())
    pairs = []
    persons_list = df['V1PERSONS'].tolist()
    for row in persons_list:
        for pair in row:
            pair_string = str(pair[0]) + ", " + str(pair[1])
            pairs.append(pair_string)

    # make one column with all the pairs and value counts
    pdf = pd.DataFrame()
    pdf["edges"] = pairs
    vc = pdf["edges"].value_counts()
    #print(str(vc))
    newdf = pd.DataFrame(vc)
    print("new df: ")
    print(newdf.head(20))

    #print(str(df.head()))
    #print(str(df['V1PERSONS']))
    
    edgefile = GRAPH_DIR + "PersonsEdgeListSorted.csv"
    logging.info("writing " + edgefile)
    newdf.to_csv(edgefile, header=True, index=True, sep=",")

    # edgefile = GRAPH_DIR + "PersonsEdgeListSorted.csv"
    # logging.info("writing " + edgefile)
    # with open(edgefile, 'w') as file:  
    #     for plist in persons_list:
    #         for pair in plist:
    #             file.write(str(pair) + "\n")
 

if __name__ == '__main__':
    main()
    print("DONE\n")


