# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 13:38:48 2020

@author: Rolf Madsen
"""


"""  ========== * Hitcount * ========== """

def getHitcount(searchResponse, fieldname, collectionindex, recordindex, fieldindex):
    try:
        hitcount = searchResponse['searchResponse']['result']['hitCount']['$']
        return hitcount
        #print(f"A search for the query '{query}' has {hitcount} hits, and the first title is {title}!")
    except KeyError:
        return f"The field {fieldname} is unknown"
    

""" ========== * Titel * ========== """ 
    
def getTitle(searchResponse, fieldname, collectionindex, recordindex, fieldindex):
    try:
        #hitcount = searchResponse['searchResponse']['result']['hitCount']['$']
        title = searchResponse['searchResponse']['result']['searchResult'][collectionindex]['collection']['object'][recordindex]['record']['title'][fieldindex]['$']
        return title
        #print(f"A search for the query '{query}' has {hitcount} hits, and the first title is {title}!")
    except KeyError:
        return f"The field {fieldname} is unknown"



""" ========== * SWITCH FUNCTION * ========== """
  
# Initieret af getField(searchResponse, title, 0, 0, 0)      
def getField(searchResponse, fieldname, collectionindex, recordindex, fieldindex):
    switcher = {
            'hitcount': getHitcount(searchResponse, 'hitcount', collectionindex, recordindex, fieldindex),
            'title': getTitle(searchResponse, 'title', collectionindex, recordindex, fieldindex),
    }
    getfieldtype = switcher.get(fieldname, lambda: "Missing field")
    return getfieldtype
