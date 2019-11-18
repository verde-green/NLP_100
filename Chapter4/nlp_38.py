# -*- coding: utf-8 -*-

import nlp_30
from collections import Counter
from matplotlib import pyplot as plt

counter = Counter()
for l in nlp_30.morpheme():
    counter.update([m["surface"] for m in l if m["pos"] != "記号"])

# フォントの設定 デフォルトだと日本語非対応
plt.rcParams["font.family"] = "Meiryo"

plt.title("単語の出現頻度のヒストグラム")
plt.xlabel("出現頻度(出現回数)")
plt.ylabel("単語の種類数")

data = [c[1] for c in counter.most_common()]
# print(Counter(data).most_common())

# ヒストグラム
plt.hist(data, bins=20, range=(1, 20))
plt.show()
