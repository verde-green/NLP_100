# -*- coding: utf-8 -*-

import plyvel
import gzip
import json
import re

db = plyvel.DB("artist.ldb")

# データベースの更新
with gzip.open("artist.json.gz", "rt") as f:
    for d in f:
        data = json.loads(d)
        
        # 重複回避
        key = data["name"] + "\t" + str(data["id"])
        
        # tags は無いこともある
        db.put(key.encode("utf-8"), json.dumps(data.get("tags", [])).encode("utf-8"))

print(len(list(db.iterator())))

# 検索
print("アーティスト名を入力")
name = input(">> ")

pattern = re.compile(rf"({name})\t(\d+)")

for k, v in db.iterator(start=name.encode("utf-8"), stop=str(name + r"\t").encode("utf-8"), include_stop=True):
    result = pattern.match(k.decode("utf-8"))

    if result:
        print(f"{result.group(1)}(id: {result.group(2)})のタグ情報")
        value = json.loads(v.decode("utf-8"))

        if value:
            for d in value:
                print(f"{d['value']} ({d['count']})")
        else:
            print("タグ情報が見つかりません")

        print("-"*10)
