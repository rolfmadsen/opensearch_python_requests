#-*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:21:16 2020

@author: Rolf Madsen
"""
# ========== * IMPORTED MODULES * ==========

import json
from time import sleep
from opensearch.search import getsearchresult
from opensearch.fields import getField


# ========== * JSON FILE WITH 10 QUERY STRINGS * ==========

with open('data/mostfrequentqueries.json', 'r', encoding='utf-8') as f:
    querylist = json.load(f)


""" ========== * LOOP OVER QUERY STRINGS FROM JSON FILE * ========== """

for row in querylist['queries']: 
    query = row['query']
    #print(f"Søgestrengen er {query}")

    objectFormat = 'dkabm'
    searchResponse = getsearchresult(query, objectFormat)
    #print(searchResponse)
    #print("searchResponse is of the type", type(response_dict))

    """ # ========== * FIELDS * ========== """
    # getTitle(searchResponse, fieldname, collectionindex, recordindex, fieldindex)
 
    hitcount = getField(searchResponse, 'hitcount', 0, 0, 1)
    title = getField(searchResponse, 'title', 0, 0, 1)

    """ # ========== * OUTPUT * ========== """
       
    print("=====¤=====")
    print(f"Search query: '{query}'")
    print(f"Hits: {hitcount}")
    print(f"The first title is: {title}")
    
    sleep(1)
