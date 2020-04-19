#-*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:21:16 2020

@author: Rolf Madsen
"""

""" ========== * IMPORTED MODULES * ========== """
import json
from opensearch.search import getsearchresult
#from opensearch.config import config

""" ==================== * =============== * ==================== """
""" ==================== * SEARCH RESPONSE * ==================== """
""" ==================== * =============== * ==================== """

query = "bc='*' and facet.typecategory='film' and facet.type='blu-ray'"
#config['query_film']
objectFormat = 'marcxchange'
#config['objectFormat']
search_response = getsearchresult(query, objectFormat)


""" ==================== * ============ * ==================== """
""" ==================== * SEARCHRESULT * ==================== """
""" ==================== * ============ * ==================== """

search_result_info = search_response['searchResponse']['result']
collection_list = search_response['searchResponse']['result']['searchResult']

""" ========== * CREATE SEARCH_RESULT_DICTIONARY * ========== """
search_result_dictionary = {}


search_result_dictionary['search_result_info'] = {}

hitcount = search_result_info['hitCount']['$']
search_result_dictionary['search_result_info']['hitcount'] = hitcount

collection_count = search_result_info['collectionCount']['$']
search_result_dictionary['search_result_info']['collection_count'] = collection_count


search_result_dictionary['search_result'] = {}


""" ==================== * =============== * ==================== """
""" ==================== * WORKCOLLECTIONS * ==================== """
""" ==================== * =============== * ==================== """

for collection in collection_list:
    collection_info = collection['collection']
    manifestation_list = collection['collection']['object']    
    
    
    """ ========== * ADD TO DICTIONARY * ========== """
    collection_position = collection['collection']['resultPosition']['$']


    """ ==================== * ============== * ==================== """
    """ ==================== * MANIFESTATIONS * ==================== """
    """ ==================== * ============== * ==================== """
    for manifestation in manifestation_list:
        manifestation_info = manifestation['collection']['record']
        field_list = manifestation['collection']['record']['datafield']
        
        
        """ ========== * ADD PID TO DICTIONARY OF EACH WORK-COLLECTIONS  * ========== """
        # print(f" \n ===== * PID *===== \n {manifestation['primaryObjectIdentifier']['$']} \n")
        pid = manifestation['primaryObjectIdentifier']['$']
        search_result_dictionary['search_result'][pid] = {}
        search_result_dictionary['search_result'][pid]['collection_position'] = collection_position
        manifestation_position = collection['collection']['resultPosition']['$']

        
        """ ==================== * ================== * ==================== """
        """ ==================== * FIELDS & SUBFIELDS * ==================== """
        """ ==================== * ================== * ==================== """       
        
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
                    continue
                try:
                    subfieldvalue = field['subfield']['$'].replace('¤', '')
                except:
                    continue
                
                """ ========== * ADD FIELD, SUBFIELD AND VALUE TO DICTIONARY * IF FIELD IS AN OBJECT * ========== """
                # print(f"'{fieldname}*{subfieldname}':'{subfieldvalue}'")
                field = f"{fieldname}*{subfieldname}"
                search_result_dictionary['search_result'][pid][field] = subfieldvalue
                
            else:
                for subfield in subfield_list:
                    try:
                        subfieldname = subfield['@code']['$']
                    except:
                        continue
                    try: 
                        subfieldvalue = subfield['$'].replace('¤', '')
                    except:
                        continue
                    
                    """ ========== * ADD FIELD, SUBFIELD AND VALUE TO DICTIONARY * IF FIELD IS A LIST * ========== """
                    # print(f"'{fieldname}*{subfieldname}':'{subfieldvalue}'")
                    field = f"{fieldname}*{subfieldname}"
                    search_result_dictionary['search_result'][pid][field] = subfieldvalue
                 
                    
print(json.dumps(search_result_dictionary, indent=4, ensure_ascii=False))
