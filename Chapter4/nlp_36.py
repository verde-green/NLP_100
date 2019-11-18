# -*- coding: utf-8 -*-

import nlp_30
from collections import Counter

counter = Counter()
for l in nlp_30.morpheme():
    counter.update([m["surface"] for m in l if m["pos"] != "記号"])

for i, c in enumerate(counter.most_common()):
    if i < 5:
        print(c)
