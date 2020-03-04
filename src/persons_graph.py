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



def update_edge_list(doc_edge_list, big_edge_list):

    new_edges = []

    for de in doc_edge_list:

        idx = index_of_edge(big_edge_list, de)
        if idx == -1:
            new_edges.append(de)
        else:
            e = big_edge_list[idx]
            e['strength'] += 1

    return big_edge_list + new_edges
 



# edge direction not considered
def same_edge(e1, e2):

    if (e1['to'] == e2['to']) and (e1['from'] == e2['from']):
        return True

    if (e1['from'] == e2['to']) and (e1['to'] == e2['from']):
        return True

    return False


def index_of_edge(elist, edge):

    for e in elist:
        if same_edge(e, edge) is True:
            return elist.index(e)
    
    return -1



def make_doc_edge_list(persons_dict, doc):

    persons_list = list(get_persons_set(doc))

    edge_list = []
    for person in persons_list:
        # make other persons list
        others = persons_list.copy()
        others.remove(person)
        # build edges to others
        for other_person in others:
            edge = {
                   'to': persons_dict[other_person][1],
                    'from': persons_dict[person][1],
                    'strength': 1
                   }

            if index_of_edge(edge_list, edge) == -1:
                edge_list.append(edge)

    return edge_list

    

def main():

    # create blank full df
    df = pd.DataFrame(columns=GKG_COLUMN_NAMES)

    #file_list = glob.glob(ARMY_GKG_DAILY_DIR + "Army_GKG_by_day*.csv")
    file_list = glob.glob(ARMY_GKG_DAILY_DIR + "Army_GKG_by_day_2020-02-16.csv")

    for f in file_list:
        
        logging.info("reading" + f)

        # read the file into temp df
        tdf = pd.read_csv(f, header=0, sep='\t', names=GKG_COLUMN_NAMES, 
            index_col=False)

        # append temp df to full df
        df = df.append(tdf, ignore_index=True)


    logging.info("consolidated df shape: " + str(df.shape))

    # build a list of the V1PERSONS column
    persons_rows = df['V1PERSONS'].tolist()


    # DEBUG
    # persons_rows = []
    # persons_rows.append("n1; n2; n3; n4")
    # persons_rows.append("n1; n3; n5; n6")
    # persons_rows.append("n1; n3;")
    
    

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



    # build edge list
    logging.info("building edge list")
    big_edge_list = []
    rows_processed = 0
    for line in persons_rows:
        doc_edge_list = make_doc_edge_list(persons_dict, line)
        #write_edge_list(doc_edge_list)
        # SLOW?
        big_edge_list = update_edge_list(doc_edge_list, big_edge_list)

        rows_processed += 1
        if (rows_processed % 10) == 0:
            logging.info("rows processed: " + str(rows_processed))
        


    edge_list_df = pd.DataFrame(big_edge_list, columns=['from', 'to', 'strength'])
    edge_list_df = edge_list_df.sort_values(by=['strength'], ascending=False)
    print(str(edge_list_df.head(20)))

    #print(str(themes_hist_df.head(500)))
    edgefile = GRAPH_DIR + "PersonsEdgeListSorted.csv"
    logging.info("writing " + edgefile)
    edge_list_df.to_csv(edgefile, header=True, index=False, sep=";")

       

if __name__ == '__main__':
    main()
    print("DONE\n")


