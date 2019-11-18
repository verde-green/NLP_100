# -*- coding: utf-8 -*-

import nlp_30

phrase = []
for l in nlp_30.morpheme():
    for i, m in enumerate(l):
        try:
            if m["surface"] == "の" and l[i-1]["pos"] == "名詞" and l[i+1]["pos"] == "名詞":
                phrase.append(l[i-1]["surface"] + m["surface"] + l[i+1]["surface"])
        except IndexError:
            continue

for i, p in enumerate(phrase):
    if i < 5:
        print(p)
