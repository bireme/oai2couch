#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from urllib import urlencode
from lxml import etree

from oaipmh import client

class CustomBaseClient(client.BaseClient):
    
    def buildRecords(self,
                     metadata_prefix, namespaces, metadata_registry, tree):
        # first find resumption token if available
        evaluator = etree.XPathEvaluator(tree,
                                         namespaces=namespaces)
        token = evaluator.evaluate(
            'string(/oai:OAI-PMH/*/oai:resumptionToken/text())')
        if token.strip() == '':
            token = None
        record_nodes = evaluator.evaluate(
            '/oai:OAI-PMH/*/oai:record')
        result = []
            
        for record_node in record_nodes:
            record_evaluator = etree.XPathEvaluator(record_node, 
                                                    namespaces=namespaces)
            e = record_evaluator.evaluate
            # find header node
            header_node = e('oai:header')[0]
            # create header
            header = buildHeader(header_node, namespaces)
            # find metadata node
            metadata_list = e('oai:metadata')
            if metadata_list:
                metadata_node = metadata_list[0]
                # create metadata
                metadata = metadata_registry.readMetadata(metadata_prefix,
                                                          metadata_node)
            else:
                metadata = None
            # XXX TODO: about, should be third element of tuple
            result.append((header, metadata, None))
        
        if self._debug:
            print "Next resumptionToken: %s" % token
    
        return result, token


class ClientOAI(CustomBaseClient):
    
    def __init__(
            self, base_url, metadata_registry=None, credentials=None, debug=None):
        CustomBaseClient.__init__(self, metadata_registry)
        self._base_url = base_url
        if credentials is not None:
            self._credentials = base64.encodestring('%s:%s' % credentials)
        else:
            self._credentials = None
        
        self._debug = debug
            
    def makeRequest(self, **kw):
        """Actually retrieve XML from the server.
        """
        # XXX include From header?
        headers = {'User-Agent': 'pyoai'}
        if self._credentials is not None:
            headers['Authorization'] = 'Basic ' + self._credentials.strip()
        request = urllib2.Request(
            self._base_url, data=urlencode(kw), headers=headers)
        return client.retrieveFromUrlWaiting(request)


def buildHeader(header_node, namespaces):
    e = etree.XPathEvaluator(header_node, 
                            namespaces=namespaces).evaluate
    identifier = e('string(oai:identifier/text())')
    datestamp = e('string(oai:datestamp/text())')
    setspec = [str(s) for s in e('oai:setSpec/text()')]
    deleted = e("@status = 'deleted'") 
    return client.common.Header(identifier, datestamp, setspec, deleted)

