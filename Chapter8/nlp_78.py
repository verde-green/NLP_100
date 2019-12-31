# -*- coding: utf-8 -*-

from nltk.stem.porter import PorterStemmer as PS
import numpy as np

import re

stop_words = "a, able, about, across, after, all, almost, also, am, among, an, and," \
        " any, are, as, at, be, because, been, but, by, can, cannot, could, dear, " \
        "did, do, does, either, else, ever, every, for, from, get, got, had, has, " \
        "have, he, her, hers, him, his, how, however, i, if, in, into, is, it, its, " \
        "just, least, let, like, likely, may, me, might, most, must, my, neither, no, " \
        "nor, not, of, off, often, on, only, or, other, our, own, rather, said, say, " \
        "says, she, should, since, so, some, than, that, the, their, them, then, " \
        "there, these, they, this, tis, to, too, twas, us, wants, was, we, were, " \
        "what, when, where, which, while, who, whom, why, will, with, would, yet, " \
        "you, your,".split(", ")

# 記号もストップワードに
stop_words.extend([".", ",", ":", ";", "!", "?", "-", "--", "(", ")", "\"", "\'"])
# re用
symbol = [".", ",", ":", ";", "!", "?", "\-", "(", ")", "\"", "\'"]

def isStopWord(word: str) -> bool:
    # ストップワードならTrue
    return  word.lower() in stop_words


def my_sub(word: str) -> str:
    # 記号を削除
    return re.sub(f"[{''.join(symbol)}]", "", word)


def load_features() -> dict:
    """
    stem_words.txtの素性リストを辞書形式へ

    Returns
    -------
    dict
        key : 素性
        value : インデックス
    """

    with open("stem_words.txt") as f:
        return {l.strip(): i for i, l in enumerate(f, 1)}


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
     

def sig(x, beta):
    # シグモイド関数
    # 説明変数xとパラメータbetaから、目的変数y=1となる確率を出力
    return 1 / (1 + np.exp(-x.dot(beta)))


def likelihood(data_x, data_y, beta) -> float:
    """
    対数尤度を計算

    Parameters
    ----------
    data_x : np.ndarray
        学習データ

    data_y : np.ndarray
        正解データ

    beta : np.ndarray
        パラメータ

    Returns
    -------
    float
        対数尤度
    """
    
    # 数字が大きいので平均とった
    return np.sum(data_y * np.log(p) + (1 - data_y) * np.log(1 - p)) / data_x.shape[0]


def renew(data_x, data_y, beta, eta) -> np.ndarray:
    """
    パラメータの更新
    確率的勾配降下法で更新

    Parameters
    ----------
    data_x : np.ndarray
        学習データ

    data_y : np.ndarray
        正解データ

    beta : np.ndarray
        更新するパラメータ

    eta : float
        学習率

    Returns
    -------
    beta : np.ndarray
        更新後のパラメータ
    """

    N = data_x.shape[0]
    
    l = list(range(N))
    np.random.shuffle(l)
    
    for i in l:
        beta -= eta * (sig(data_x[i], beta) - data_y[i]) * data_x[i]

    return beta


# 改変
def learn(data_x, data_y, beta, eta, num) -> np.array:
    """
    ロジスティック回帰の学習

    Parameters
    ----------
    data_x : np.ndarray
    data_y : np.ndarray
        正解データ

    beta : np.ndarray
        パラメータ

    eta : float
        学習率

    num : int
        学習回数

    Returns
    -------
    beta : np.ndarray
        学習後のパラメータ
    """

    for i in range(num):
        beta = renew(data_x, data_y, beta, eta)
        
        # イテレーション毎に学習率を低下
        eta *= 0.9

        if (i + 1) % 100 == 0:
            print(f"#{i+1} Likelihood: {likelihood(data_x, data_y, beta)}")

    return beta


def score(data_x, data_y, beta):
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
    """

    TP = 0      # True-Positive
    TN = 0      # True-Negative
    FP = 0      # False-Positive
    FN = 0      # False-Negative

    result = [1 if sig(x, beta) >= 0.5 else 0 for x in data_x]

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

    print(f"正解率: {accuracy}\n適合率: {precision}\n再現率: {recall}\nF1スコア: {f1}")


def cross_validation(eta, num, split_size=5):
    """
    交差検定をする関数

    Parameters
    ----------
    eta : float
        学習率

    num : int
        学習回数

    split_size : int
        交差検定する際の分割数
    """

    data_x, data_y = make_training_data()
    data_x = np.array([x for x in data_x])


    # 今回は学習データ(＆検証データ)とテストデータを8:2くらいに分割
    # 学習データ: 8000件 テストデータ: 残り
    
    # 重複なしの乱数を2662個生成 -> テストデータのインデックス
    np.random.seed()
    l = set()
    while len(l) < 2662:
        l.add(np.random.randint(0, data_y.shape[0]+1))

    test_x = np.array([data_x[i] for i in l])
    test_y = np.array([data_y[i] for i in l])

    train_x = np.array([x for i, x in enumerate(data_x) if i not in l])
    train_y = np.array([y for i, y in enumerate(data_y) if i not in l])
    

    beta = np.random.randn(train_x.shape[1])


    # 分割
    train_x = np.array_split(train_x, split_size)
    train_y = np.array_split(train_y, split_size)

    
    for i in range(split_size):
        print(f"{i+1}回目\n" + "-"*30)

        merged_x = np.concatenate([x for j, x in enumerate(train_x) if j != i])
        merged_y = np.concatenate([y for j, y in enumerate(train_y) if j != i])

        print(merged_x.shape)
        print(merged_y.shape)

        beta = learn(merged_x, merged_y, beta, eta, num)
        
        print()
        score(train_x[i], train_y[i], beta)

    print("\nテストデータでのスコア")
    score(test_x, test_y, beta)

    # 学習結果を保存
    np.save("cross_beta.npy", beta)


features  = load_features()
ps = PS()

if __name__ == "__main__":
    eta = 0.1
    num = 1000
    # learn(eta, num)
    cross_validation(eta, num, 5)
