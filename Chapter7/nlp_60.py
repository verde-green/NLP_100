# -*- coding: utf-8 -*-

# LevelDBのライブラリの１つ
import plyvel
import gzip
import json

db = plyvel.DB("artist.ldb", create_if_missing=True)

with gzip.open("artist.json.gz", "rt") as f:
    for d in f:
        data = json.loads(d)
        
        # キーが重複することがあるので識別子追記
        # 空白でつなげると検索の際に"key 2"とかにマッチしそうなのでタブで
        key = data["name"] + "\t" + str(data["id"]) 

        # areaが無いこともある
        db.put(key.encode("utf-8"), data.get("area", "").encode("utf-8"))

# artist.jsonのデータ数は921337
print(len(list(db.iterator())))
