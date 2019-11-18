# -*- coding: utf-8 -*-

def morpheme() -> list:
    # neko.txt.mecab : $ cat neko.txt | mecab > neko.txt.mecab
    with open("./neko.txt.mecab") as f:
        line = f.readlines()

    morphemes = []
    m = []
    for l in line:
        if l == "EOS\n":
            if m:
                morphemes.append(m)
                m = []
            continue

        else:
            r = l.split("\t")
            r[1] = r[1].split(",")
            m.append({"surface": r[0], "base": r[1][6], "pos": r[1][0], "pos1": r[1][1]})

    return morphemes


if __name__ == "__main__":
    m = morpheme()
    print(m[0])
    print(m[1])
