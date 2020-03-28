# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 13:04:19 2020

@author: Rolf Madsen
"""
 
import requests
# REFERENCE - https://requests.readthedocs.io/en/master/

#  Request body and parameters
# - https://oss-services.dbc.dk/opensearch/5.0/?action=search&query=%22danmark%22&agency=100200&profile=test&start=1&stepValue=5

def getsearchresult(query):
    
    querystring = f"\"{query}\""

    parameters = {
        'action':'search',
        'query':querystring,
        'agency':'100200',
        'profile':'test',
        'start':'1',
        'stepValue':'5',
        'outputType':'json'
    }
    
    endpoint = 'https://oss-services.dbc.dk/opensearch/5.2/?'
    
    response = requests.get(
        url=endpoint, 
        params=parameters,
        )
    
    response_dict = response.json()
    
    #print(response.url)

    return response_dict
