# -*- coding: utf-8 -*-

import nlp_30
from collections import Counter
from matplotlib import pyplot as plt

counter = Counter()
for l in nlp_30.morpheme():
    counter.update([m["surface"] for m in l if m["pos"] != "記号"])

# フォントの設定 デフォルトだと日本語非対応
plt.rcParams["font.family"] = "Meiryo"

plt.title("単語の出現頻度上位10語")
plt.xlabel("単語")
plt.ylabel("出現頻度(出現回数)")

x = [c[0] for c in counter.most_common(10)]
y = [c[1] for c in counter.most_common(10)]

# 棒グラフ
plt.bar(x, y)
plt.show()
