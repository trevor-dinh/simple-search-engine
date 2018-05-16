from pymongo import MongoClient
from pprint import pprint
import urllib

USERNAME = "***REMOVED***"
PASSWORD = "***REMOVED***"
CNTSTR =  ***REMOVED***.format(
    urllib.quote(USERNAME), urllib.quote(PASSWORD))

print(CNTSTR)
client = MongoClient(CNTSTR)
print(client.test_database)

