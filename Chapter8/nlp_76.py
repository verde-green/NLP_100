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


def predict(text: str) -> str:
    """
    与えられた文章の極性を予測

    Parameters
    ----------
    text : str
        極性分析したい文章

    Returns
    -------
    str
        正解ラベル \t 予測ラベル \t 予測確率
    """

    beta = np.load("beta.npy")
    
    data_x = extract_features(text[3:])
    p = sig(data_x, beta)
        
    label = ["+1", p] if p >= 0.5 else ["-1", 1-p]

    return f"{text[:2]}\t{label[0]}\t{label[1]}\n"
        

with open("stem_words.txt") as f:
    features = {l.strip(): i for i, l in enumerate(f, 1)}

ps = PS()

if __name__ == "__main__":
    with open("sentiment.txt") as f:
        with open("result_nlp_76.txt", "w") as r:
            r.writelines(map(predict, f))
