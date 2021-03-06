# -*- coding: utf-8 -*-

import gzip
import json

with gzip.open("jawiki-country.json.gz", "rt") as f:
    for l in f:
        data = json.loads(l)
        if data["title"] == "イギリス":
            break

data = [d for d in data["text"].split("\n") if "[[Category:" in d]
[print(d) for d in data]
