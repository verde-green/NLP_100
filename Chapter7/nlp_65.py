# -*- coding: utf-8 -*-

from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.artist
collection = db.artist

for d in collection.find({"name": "Queen"}):
    pprint(d)
    print("-"*10)
