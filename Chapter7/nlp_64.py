# -*- coding: utf-8 -*-

from pymongo import MongoClient, ASCENDING
import gzip
import json

client = MongoClient()

# 無ければ生成
db = client.artist
collection = db.artist

# バルクインサートの単位
bulk = 10000
buf = []
with gzip.open("artist.json.gz", "rt") as f:
    for i, d in enumerate(f, 1):
        data = json.loads(d)
        buf.append(data)

        if i % bulk == 0:
            collection.insert_many(buf)
            buf.clear()

        print(f"\r{i}/921337", end="")

    if buf:
        collection.insert_many(buf)

collection.create_index([("name", ASCENDING)])
collection.create_index([("aliases.name", ASCENDING)])
collection.create_index([("tags.value", ASCENDING)])
collection.create_index([("rating.value", ASCENDING)])
