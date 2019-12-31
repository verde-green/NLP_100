# -*- coding: utf-8 -*-

from nltk.stem.porter import PorterStemmer as PS
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


if __name__ == "__main__":
    words = []
    ps = PS()
    with open("sentiment.txt") as f:
        for l in f:
            # ストップワードの除去
            # 1文字の単語も除く
            words.extend([ps.stem(my_sub(w.strip())) for w in l.split(" ")[1:] if not isStopWord(w) and len(my_sub(w.strip())) > 1])

    with open("stem_words.txt", "w") as f:
        f.write("\n".join([w for w in set(words) if w]))
