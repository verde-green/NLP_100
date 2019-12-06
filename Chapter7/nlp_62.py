# -*- coding: utf-8 -*-

import plyvel

db = plyvel.DB("artist.ldb")
target = "Japan".encode("utf-8")
print(len([1 for k, v in db.iterator() if v == target]))
