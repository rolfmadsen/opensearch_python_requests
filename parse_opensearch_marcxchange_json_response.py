#-*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:21:16 2020

@author: Rolf Madsen
"""

""" ========== * IMPORTED MODULES * ========== """

# from time import sleep # SET REQUEST LIMIT TO X SECONDS
from opensearch.search import getsearchresult
# from opensearch.fieldsMarcxchange import getField


""" ========== * OPENSEARCH REQUEST * ========== """
query = "bc='*' and facet.typecategory='film' and facet.type='blu-ray'"

objectFormat = 'marcxchange'
searchResponse = getsearchresult(query, objectFormat)


""" ========== * SEARCHRESULT OF OPENSEARCH RESPONSE * ========== """
searchresult = searchResponse['searchResponse']['result']['searchResult']


""" ========== * LOOP THROUGH WORK-COLLECTIONS OPENSEARCH RESPONSE * ========== """
collection_list = searchresult
for collection in collection_list:
    
    
    """ ========== * LOOP THROUGH MANIFESTATIONS / OBJECTS IN EACH WORK-COLLECTIONS  * ========== """
    manifestation_list = collection['collection']['object']
    for manifestation in manifestation_list:
        
        """ ========== * PRINT PID OF EACH WORK-COLLECTIONS  * ========== """
        print(f" \n ===== * PID *===== \n {manifestation['primaryObjectIdentifier']['$']} \n")

        
        """ ========== * LOOP THROUGH FIELDS IN EACH MANIFESTATION / OBJECT IN EACH WORK-COLLECTIONS  * ========== """
        field_list = manifestation['collection']['record']['datafield']
        for field in field_list:
        
            """ ========== * FIELDNAME - FX "001"  * ========== """
            fieldname = field['@tag']['$']
            
            """ ========== * SUBFIELDNAME - FX "a" * ========== * SUBFIELDVALUE - FX "6140793" * ========== """
            subfield_list = field['subfield']
            subfield_list_is_dict = isinstance(subfield_list, dict)
            if subfield_list_is_dict:
                try:
                    subfieldname = field['subfield']['@code']['$']
                except:
                    subfieldname = ""
                try:
                    subfieldvalue = field['subfield']['$'].replace('¤', '')
                except:
                    continue
                
                """ ========== * PRINT FIELD, SUBFIELD AND VALUE * IF FIELD IS AN OBJECT * ========== """
                print(f"'{fieldname}*{subfieldname}':'{subfieldvalue}'")
                
            else:
                for subfield in subfield_list:
                    try:
                        subfieldname = subfield['@code']['$']
                    except:
                        subfieldname = ""
                    try: 
                        subfieldvalue = subfield['$'].replace('¤', '')
                    except:
                        continue
                    
                    """ ========== * PRINT FIELD, SUBFIELD AND VALUE * IF FIELD IS A LIST * ========== """
                    print(f"'{fieldname}*{subfieldname}':'{subfieldvalue}'")
