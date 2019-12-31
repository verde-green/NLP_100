# -*- coding: utf-8 -*-

TP = 0      # True-Positive
TN = 0      # True-Negative
FP = 0      # False-Positive
FN = 0      # False-Negative

with open("result_nlp_76.txt") as f:
    # 集計
    for l in f:
        c = l.split("\t")

        if c[0] == "+1" and c[1] == "+1":
            TP += 1
        
        elif c[0] == "+1" and c[1] == "-1":
            FN += 1

        elif c[0] == "-1" and c[1] == "+1":
            FP += 1

        elif c[0] == "-1" and c[1] == "-1":
            TN += 1

    # 各種計算
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * precision * recall / (precision + recall)

    print(f"正解率: {accuracy}")
    print(f"適合率: {precision}")
    print(f"再現率: {recall}")
    print(f"F1スコア: {f1}")
