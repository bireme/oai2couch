#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re
import json 

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from couchdbkit import *
from optparse import OptionParser

import settings

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


def save_in_couch(provider):
    provider_name, provider_url = provider
    
    client = Client(provider_url, registry)    
    count = 0
    try:
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

            if count >= settings.MAX_DOCS_TO_HARVEST:
                print('Harvest of ' + provider_name + ' Done.')
                break;

    except Exception, detail:
        print('Harvest of ' + provider_name + ' FAIL ===>' + str(detail))


#######################################################################################

# allow execute a script for a specific provider defined in settings provider list

parser = OptionParser()
parser.add_option("-n", type="int", dest="provider_num")

(options, args) = parser.parse_args()

# server object 
server = Server(settings.COUCH_SERVER)

# create or associate to couch database
db = server.get_or_create_db(settings.COUCH_DB)

registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)

if options.provider_num != None:
    provider_num_index = options.provider_num - 1 
    
    try:
        provider = settings.PROVIDERS[provider_num_index]
        save_in_couch(provider)
        
    except IndexError, e:
        print('Provider number not available in settings provider list')
    
else:
    for provider in settings.PROVIDERS:
        save_in_couch(provider)
