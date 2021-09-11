import json
from backend.couchDbHandler import *

cdb = CouchDB()
#couchDbHandler = cdb.create_db('ccc')
all_db = cdb.get_db('melbourne2016')
table_all = all_db.view('_design/dictionary/_view/language', key = 'en', limit = 10)

for i in table_all:
    print(i)

