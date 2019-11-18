# -*- coding: utf-8 -*-

import nlp_30

verbs = [m for l in nlp_30.morpheme() for m in l if m["pos"] == "動詞"]

for i, v in enumerate(verbs):
    if i < 5:
        print(v["surface"])
