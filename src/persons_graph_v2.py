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


# return persons set from a string of gkg v1 persons
def get_persons_set(persons_line):

    persons_set = set()
    l = persons_line.strip()
    person_list = l.split(";")
    
    for person in person_list:
        person = person.strip()
        if len(person) > 1:
            persons_set.add(person)

    return persons_set


def make_persons_pairs(persons_line):

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


def names_to_ids(row):
    print(row.name)
    #print(str(row))
    


def main():

    # # create blank full df
    # df = pd.DataFrame(columns=GKG_COLUMN_NAMES)

    # file_list = glob.glob(ARMY_GKG_DAILY_DIR + "Army_GKG_by_day*.csv")
    # #file_list = glob.glob(ARMY_GKG_DAILY_DIR + "Army_GKG_by_day_2020-02-16.csv")

    # for f in file_list:
        
    #     logging.info("reading" + f)

    #     # read the file into temp df
    #     tdf = pd.read_csv(f, header=0, sep='\t', names=GKG_COLUMN_NAMES, 
    #         index_col=False)

    #     # append temp df to full df
    #     df = df.append(tdf, ignore_index=True)


    # logging.info("consolidated df shape: " + str(df.shape))


    # -------------------------------- DEBUG ------------------------------
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
    df = pd.DataFrame(gkg_data, columns=GKG_COLUMN_NAMES)



    # ------ create person nodes (TODO this can be made faster) --------
    persons_rows = df['V1PERSONS'].tolist()
    persons_dict = {}

    # assign person IDs
    pid = 0
    persons_set = set()
    for line in persons_rows:
        persons_set = get_persons_set(line)

        for person in persons_set:
            if person in persons_dict.keys():
                values = persons_dict[person]
                node_size = values[0]
                person_id = values[1]
                persons_dict[person] = [node_size + 1, person_id]

            else:
                persons_dict[person] = [1, pid]
                pid += 1


    # convert, sort and write person nodes file
    plist = []
    for key, value in persons_dict.items():   
        pl = [value[1], key, value[0]]
        plist.append(pl)

    node_list_df = pd.DataFrame(plist, columns=['id', 'label', 'value'])
    node_list_df = node_list_df.sort_values(by=['value'], ascending=False)
    print(str(node_list_df.head(20)))   

    nodesfile = GRAPH_DIR + "PersonsNodes.csv"
    logging.info("writing " + nodesfile)
    node_list_df.to_csv(nodesfile, header=True, index=False, sep=";")    


    # -------------------- Build edge list ------------------------------------


    # make persons column into set
    df['V1PERSONS'] = df.apply(lambda row: make_persons_pairs(row.V1PERSONS), axis=1)

    # pdf = df[['V1PERSONS']].copy()
    # print(pdf.head())
    logging.info('creating pairs')
    pairs = []
    persons_list = df['V1PERSONS'].tolist()
    for row in persons_list:
        for pair in row:
            pair_string = str(pair[0]) + ", " + str(pair[1])
            pairs.append(pair_string)

    # make one column with all the pairs and value counts
    logging.info('building edge df')
    pdf = pd.DataFrame()
    pdf["edges"] = pairs
    vc = pdf["edges"].value_counts()
    edge_df = pd.DataFrame(vc)
    print("edge df: ")
    print(edge_df.head(20))

    #print(str(df.head()))
    #print(str(df['V1PERSONS']))
    
    edgefile = GRAPH_DIR + "PersonsEdgeListSorted.csv"
    logging.info("writing " + edgefile)
    edge_df.to_csv(edgefile, header=True, index=True, sep=",")


    # Write the edge list using node ids instead of names
    edge_df['ids'] = edge_df.apply(lambda row: names_to_ids(row), axis=1)

    # edgefile = GRAPH_DIR + "PersonsEdgeListSorted.csv"
    # logging.info("writing " + edgefile)
    # with open(edgefile, 'w') as file:  
    #     for plist in persons_list:
    #         for pair in plist:
    #             file.write(str(pair) + "\n")
 

if __name__ == '__main__':
    main()
    print("DONE\n")


