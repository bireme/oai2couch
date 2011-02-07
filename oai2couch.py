#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re
import json 

from settings import *

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from couchdbkit import *

class Provider():
    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint
    

def remove_empty_keys(dictionary):

    no_empty_dict = dict()
    valid_value_list = list()

    for key,value in dictionary.items():
        if value:
            if isinstance(value, list) and len(value) > 0:
                valid_values_list = [v for v in value if v != 'None']
                if valid_values_list:
                    no_empty_dict[key] = valid_values_list
            else:
                if value != 'None':
                    no_empty_dict[key] = value

    return no_empty_dict


def save_in_couch(provider_name):
    count = 0
    for record in client.listRecords(metadataPrefix='oai_dc'):
        
        header, metadata, about = record
        
        if metadata:
            # getMap return dictonary with all metadata fields
            doc = metadata.getMap()
            # 
            doc['_id'] = re.sub('[:/.]','-',header.identifier())
            doc['datestamp'] = str(header.datestamp())
            doc['provider'] = provider_name
            
            # only save documents that have identifier metadata
            if doc['identifier']:
                doc = remove_empty_keys(doc)
                db.save_doc(doc)
                count = count +1
        
        if count >= MAX_DOCS_TO_HARVEST:
            break;
        

#######################################################################################

# server object 
server = Server(COUCH_SERVER)

# create or associate to couch database
db = server.get_or_create_db(COUCH_DB)

for provider in PROVIDERS:
    provider_name = provider[0]
    provider_url = provider[1]

    registry = MetadataRegistry()
    registry.registerReader('oai_dc', oai_dc_reader)
    client = Client(provider_url, registry)

    save_in_couch(provider_name)
    
