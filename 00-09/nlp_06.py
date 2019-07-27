# -*- coding: utf-8 -*-

def n_gram(obj, n):
    return [obj[i:i+n:] for i  in range(len(obj) - n + 1)]

if __name__ == "__main__":
    text = ["paraparaparadise", "paragraph"]
    X = set(n_gram(text[0], 2))
    Y = set(n_gram(text[1], 2))
    se = ["True" if "se" in X else "False", "True" if "se" in Y else "False"]
    print(f"X: {X}")
    print(f"Y: {Y}")
    print(f"X | Y: {X | Y}")
    print(f"X & Y: {X & Y}")
    print(f"X - Y: {X - Y}")
    print(f'"se" in X: {se[0]}')
    print(f'"se" in Y: {se[1]}')
    
