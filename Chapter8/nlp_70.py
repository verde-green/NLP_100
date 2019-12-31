# -*- coidng: utf-8 -*-

import random

fenc="cp1252"
with open("rt-polaritydata/rt-polarity.pos", encoding=fenc) as f:
    p_data = ["+1 " + d for d in f]

with open("rt-polaritydata/rt-polarity.neg", encoding=fenc) as f:
    n_data = ["-1 " + d for d in f]

p_data.extend(n_data)
random.shuffle(p_data)

with open("sentiment.txt", "w") as f:
    f.writelines(p_data)

p = 0
n = 0
with open("sentiment.txt") as f:
    for l in f:
        if "+" == l[0]:
            p += 1
        n += 1

    print(f"p: {p} n: {n - p}")
