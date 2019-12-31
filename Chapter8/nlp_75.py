# -*- coding: utf-8 -*-

import numpy as np

with open("stem_words.txt") as f:
    features = {i: l.strip() for i, l in enumerate(f, 1)}

beta = np.load("beta.npy")

# beta_0 は切片なので素性とは関係ない重み
rank = sorted([(i, b) for i, b in enumerate(beta) if i > 0], key=lambda x: x[1])

print("重みの高い素性トップ10\n" + "-"*10)
print("\n".join([f"{i}: {features[r[0]]} ({r[1]})" for i, r in enumerate(rank[-10:][::-1], 1)]))

print("\n重みの低い素性トップ10\n" + "-"*10)
print("\n".join([f"{i}: {features[r[0]]} ({r[1]})" for i, r in enumerate(rank[:10], 1)]))
