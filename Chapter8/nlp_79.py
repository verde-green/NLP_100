# -*- coding: utf-8 -*-

import numpy as np
from nltk.stem.porter import PorterStemmer as PS
import re

from matplotlib import pyplot as plt


with open("stem_words.txt") as f:
    features = {l.strip(): i for i, l in enumerate(f, 1)}

ps = PS()

symbol = [".", ",", ":", ";", "!", "?", "\-", "(", ")", "\"", "\'"]

def my_sub(word: str) -> str:
    # 記号を削除
    return re.sub(f"[{''.join(symbol)}]", "", word)


def extract_features(line: str) -> np.ndarray:
    """
    引数の文章から素性のone-hotベクトルを生成

    Parameters
    ----------
    line : str
        one-hotベクトルの生成元の文章

    Returns
    -------
    vec : np.ndarray
        one-hotベクトル
        学習の際に切片が必要になるので、第1成分は常に1
    """

    global features     # dictionary of features
    global ps           # PorterStemmer

    vec = np.zeros(len(features) + 1)
    vec[0] = 1

    for w in line.split(" ")[1:]:
        try:
            vec[features[ps.stem(my_sub(w))]] = 1

        except KeyError:
            pass

    return vec


def make_training_data() -> np.ndarray:
    """
    sentiment.txtから学習データを生成

    Returns
    -------
    data_x : np.ndarray
        各行が素性とした単語が含まれているかどうかを表すone-hotベクトルを持つ行列

    data_y : np.ndarray
        極性ラベルの行列
    """

    with open("sentiment.txt", encoding="cp1252") as f:
        line = f.readlines()

        # ユニバーサル関数化
        ufunc = np.frompyfunc(extract_features, 1, 1)

        data_x = ufunc(line)
        data_y = np.zeros(len(line))
    
        for i, l in enumerate(line):
            if l[0] == "+":
                data_y[i] = 1

    return data_x, data_y


def sig(data_x, beta):
    return 1 / (1 + np.exp(-data_x.dot(beta)))


def score(data_x, data_y, beta, threshold) -> tuple:
    """
    正解率、適合率、再現率、F1スコアを計算

    Parameters
    ----------
    data_x : np.ndarray
        検証データ

    data_y : np.ndarray
        正解データ

    beta : np.ndarray
        学習済みパラメータ

    threshold : float
        分類の閾値

    Returns
    -------
    accuracy : float
        正解率

    precision : float
        適合率

    recall : float
        再現率

    f1 : float
        F1スコア
    """

    TP = 0      # True-Positive
    TN = 0      # True-Negative
    FP = 0      # False-Positive
    FN = 0      # False-Negative

    result = [1 if sig(x, beta) >= threshold else 0 for x in data_x]

    for x, y in zip(result, data_y):
        if x and y:
            TP += 1
        elif x:
            FP += 1
        elif y:
            FN += 1
        else:
            TN += 1

    # 各種計算
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * precision * recall / (precision + recall)

    return (accuracy, precision, recall, f1)


if __name__ == "__main__":
    data_x, data_y = make_training_data()
    
    # ランダムにテストデータを抽出
    l = set()
    while len(l) < 2662:
        l.add(np.random.randint(0, data_y.shape[0]+1))

    test_x = np.array([x for i, x in enumerate(data_x) if i in l])
    test_y = np.array([y for i, y in enumerate(data_y) if i in l])

    beta = np.load("cross_beta.npy")

    data = [score(test_x, test_y, beta, 0 + i / 10) for i in range(1, 10)]
    x = [d[1] for d in data]
    y = [d[2] for d in data]

    # グラフ関連
    plt.rcParams["font.family"] = "Meiryo"
    plt.title("分類の閾値を変化させた時の適合率-再現率グラフ")
    plt.xlabel("適合率")
    plt.ylabel("再現率")
    plt.plot(x, y)
    plt.savefig("precision_recall.png")
    plt.show()
