# -*- coding: utf-8 -*-

class Morph(object):
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    def __str__(self):
        return f"surface: {self.surface} base: {self.base} pos: {self.pos} pos1: {self.pos1}"


def read_cabocha() -> list:
    with open("./neko.txt.cabocha") as f:
        morphs = []
        for l in f:
            if l == "EOS\n":
                yield morphs
                morphs = []

            # 行頭が"*"のものは文節の開始地点のみ
            elif l[0] == "*":
                continue

            else:
                surface, other = l.split("\t")
                other = other.split(",")

                morphs.append(Morph(surface, other[6], other[0], other[1]))


if __name__ == "__main__":
    for i, r in enumerate(read_cabocha()):
        if i == 2:
            for m in r:
                print(m)
            break
