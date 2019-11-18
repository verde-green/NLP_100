# -*- coding: utf-8 -*-

import nlp_30

nouns = [m for l in nlp_30.morpheme() for m in l if m["pos"] == "名詞" and m["pos1"] == "サ変接続"]

for i, n in enumerate(nouns):
    if i < 5:
        print(n["surface"])
