# -*- coding: utf-8 -*-
import re

class Morph(object):
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    def __str__(self):
        return f"surface: {self.surface} base: {self.base} pos: {self.pos} pos1: {self.pos1}"


class Chunk(object):
    def __init__(self, morphs=None, dst=-1, srcs=None):
        self.morphs = []
        self.dst = dst
        self.srcs = []

        if morphs:
            self.morphs = morphs

        if srcs:
            self.srcs = srcs

    def __str__(self):
        c = "".join([m.surface for m in self.morphs])
        
        # return f"{c}\tdst: [{self.dst if self.dst > 0 else ''}]\tsrcs: {self.srcs}"
        return f"{c}\tdst: [{self.dst if self.dst > 0 else ''}]"

    def not_punctuation(self):
        return "".join([m.surface for m in self.morphs if m.pos != "記号"])

    def has_morph(self, pos: str) -> bool:
        for m in self.morphs:
            if m.pos == pos:
                return True

        return False
    
    # 改変
    def get_morphs(self, pos: str) -> list:
        # 品詞がposに一致するMorphオブジェクトのリストを返す

        # return [m.base for m in self.morphs if m.pos == pos]
        return [m for m in self.morphs if m.pos == pos]


# 改変
def get_case(chunks: list) -> dict:
    """
    動詞とそれに係る格の抽出

    Parameters
    ----------
    chunks : list
        Chunkオブジェクトのリスト

    Returns
    -------
    dict
        key : chunksに含まれる動詞の基本形
        value : keyの動詞に係る文節のうち助詞が含まれるChunkオブジェクト
    """

    # 動詞は最左のものをとる -> get_morphs("動詞")[0]
    # get_morphs()はリストで返ってくるので、二重ループさせて１つのリストに
    # return {c.get_morphs("動詞")[0]: 
    #        [m for s in c.srcs for m in chunks[s].get_morph] 
    #        for c in chunks if c.has_morph("動詞")}
    
    return {c.get_morphs("動詞")[0].base: 
            [chunks[s] for s in c.srcs if chunks[s].has_morph("助詞")] 
            for c in chunks if c.has_morph("動詞")}


def read_cabocha() -> list:
    with open("./neko.txt.cabocha") as f:
        # 1文をChunkオブジェクトのリストとあるが、扱いづらかったので一旦辞書型に
        chunks = {}
        c = []

        for l in f:
            if l == "EOS\n":
                yield [c[1] for c in sorted(chunks.items(), key=lambda x: x[0])]
                chunks = {}

            # 行頭が"*"のものは文節の開始地点のみ
            elif l[0] == "*":
                # (dst, srcs)
                c = list(map(int, re.findall(r"\*\s(\d+)\s(-?\d+)D", l)[0]))
                
                # 係り先の保存
                try:
                    chunks[c[0]].dst = c[1]
                except KeyError:
                    chunks[c[0]] = Chunk(dst=c[1])

                if c[1] != -1:
                    # 係り先のChunkにsrcs追加
                    try:
                        chunks[c[1]].srcs.append(c[0])
                    except KeyError:
                        chunks[c[1]] = Chunk()
                        chunks[c[1]].srcs.append(c[0])

            else:
                surface, other = l.split("\t")
                other = other.split(",")
                                
                chunks[c[0]].morphs.append(Morph(surface, other[6], other[0], other[1]))


if __name__ == "__main__":
    with open("nlp_46.txt", "w") as f:
        # 確認用
        n = int(input(">> "))

        for i, r in enumerate(read_cabocha(), 1):
            for c in get_case(r).items():
                clause = [[chunk.get_morphs("助詞")[0].base, chunk.not_punctuation()] for chunk in c[1]]
                clause = sorted(clause, key=lambda x: x[0])
                f.write(f"{c[0]}\t{' '.join([w[0] for w in clause])}\t{' '.join([w[1] for w in clause])}\n")

                if i == n:
                    print(f"{c[0]}\t{' '.join([w[0] for w in clause])}\t{' '.join([w[1] for w in clause])}")
