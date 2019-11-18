# -*- coding: utf-8 -*-

import nlp_30
from collections import Counter
from matplotlib import pyplot as plt

counter = Counter()
for l in nlp_30.morpheme():
    counter.update([m["surface"] for m in l if m["pos"] != "記号"])

# フォントの設定 デフォルトだと日本語非対応
plt.rcParams["font.family"] = "Meiryo"

plt.title("Zipfの法則")
plt.xlabel("出現頻度順位")
plt.ylabel("出現頻度(出現回数)")

data = Counter([c[1] for c in counter.most_common()]).most_common()
y = [d[1] for d in data]
x = range(1, len(y)+1)

plt.xscale("log")
plt.yscale("log")

# 散布図グラフ
plt.scatter(x, y)
plt.show()
