# -*- encoding: utf-8 -*-
# oai2couch configuration file


COUCH_SERVER = 'http://localhost:5984'
COUCH_DB = 'oai-repo'

MAX_DOCS_TO_HARVEST = 10

PROVIDERS = (
                ('IMSEAR (SEARO)', 'http://imsear.hellis.org/oai/request'),
)


