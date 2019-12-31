# -*- coding: utf-8 -*-

import numpy as np
from nltk.stem.porter import PorterStemmer as PS

import re

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
    
    global features     # load_features()
    global ps           # PorterStemmer

    vec = np.zeros(len(features) + 1)
    vec[0] = 1

    for w in line.split(" ")[1:]:
        try:
            vec[features[ps.stem(my_sub(w))]] = 1

        except KeyError:
            pass

    return vec


def sig(data_x, beta):
    return 1 / (1 + np.exp(-data_x.dot(beta)))


def predict():
    """
    与えられた文章の極性を予測
    """

    beta = np.load("beta.npy")

    while 1:
        print("極性分析したい文章を入力")
        text = input(">> ")

        data_x = extract_features(text)
        p = sig(data_x, beta)
        
        label = ["+1", "positive"] if p >= 0.5 else ["-1", "negative"]

        print(f"label: {label[0]}({label[1]}) score: {p}\n")
        

with open("stem_words.txt") as f:
    features = {l.strip(): i for i, l in enumerate(f, 1)}

ps = PS()

if __name__ == "__main__":
    predict()
