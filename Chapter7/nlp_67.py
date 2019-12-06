# -*- coding: utf-8 -*-

from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.artist
collection = db.artist

print("アーティスト名を入力してください")
name = input(">> ")

for d in collection.find({"aliases.name": name}):
    pprint(d)
    print("-"*10)
