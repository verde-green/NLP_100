# -*- coding: utf-8 -*-

import re
from nltk.stem.porter import PorterStemmer as PS

pattern = re.compile(r"(.+?[\.;:\?!])\s([A-Z].*)")

def sentence_split():
    with open("./nlp.txt") as f:
        for line in f:
            line = line.strip()

            while line:
                result = pattern.search(line)
            
                if result:
                    yield result.group(1)
                    line = result.group(2)
                else:
                    yield line
                    line = ""


def word_split():
    for s in sentence_split():
        for w in s.split(" "):
            yield w.rstrip(".,;:?!")

        # 終端で空白出力
        yield ""


def stemming():
    # 問題にあるstemmingモジュールはPython3に非対応らしい
    # Porterのステミングアルゴリズムはnltkのもので代用
    ps = PS()
    for w in word_split():
        yield [w, ps.stem(w)]

if __name__ == "__main__":
    for s in stemming():
        print(f"{s[0]}\t{s[1]}")
