# -*- coding: utf-8 -*-

def n_gram(obj, n):
    return [obj[i:i+n:] for i  in range(len(obj) - n + 1)]

if __name__ == "__main__":
    text = "I am an NLPer"
    print(n_gram(text.split(" "), 2))
    print(n_gram(text, 2))
