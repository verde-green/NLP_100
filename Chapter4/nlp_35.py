# -*- coding: utf-8 -*-

import nlp_30

junction = []
for l in nlp_30.morpheme():
    j = []
    for m in l:
        if m["pos"] == "名詞":
            j.append(m["surface"])
        elif len(j) > 1:
            junction.append("".join(j))
            j = []
        else:
            j = []

for i, j in enumerate(junction):
    if i < 5:
        print(j)
