# -*- coding: utf-8 -*-

from pymongo import MongoClient

client = MongoClient()
db = client.artist
collection = db.artist

dance = [d for d in collection.find({"tags.value": "dance"}) if "rating" in d]
top10 = [(d["name"], d["rating"]["count"]) for d in 
        sorted(dance, key=lambda x: -x["rating"]["count"])][:10]

c = 0
for i, d in enumerate(top10, 1):
    if c == d[1]:
        i -= 1

    print(f"{i}位: {d[0]} ({d[1]})")
    c = d[1]
