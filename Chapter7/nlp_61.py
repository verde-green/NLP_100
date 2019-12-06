# -*- coding: utf-8 -*-

import plyvel
import re

db = plyvel.DB("artist.ldb")


print("活動場所を検索したいアーティスト名を入力")
name = input(">> ")

pattern = re.compile(fr"{name}\t(\d+)")

# キーが name ~ name\t.+ の範囲のもののみ取り出す
for k, v in db.iterator(start=name.encode("utf-8"), stop=str(name + r"\t").encode("utf-8"), include_stop=True):
    # 完全一致のアーティスト名のみ表示
    result = pattern.match(k.decode("utf-8"))
    if result:
        if v:
            print(f"{name} (id: {result.group(1)}): {v.decode('utf-8')}")
        else:
            print(f"{name} (id: {result.group(1)}): 未登録")
