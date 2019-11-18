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

    def has_morph(self, pos: str, pos1='') -> bool:
        for m in self.morphs:
            if pos1:
                if m.pos == pos and m.pos1 == pos1:
                    return True
            else:
                if m.pos == pos:
                    return True

        return False
    
    def get_morphs(self, pos: str, pos1='') -> list:
        # 品詞がposに一致するMorphオブジェクトのリストを返す
        # pos1も指定されている場合はそっち優先
        
        if pos1:
            morphs = [m for m in self.morphs if m.pos == pos and m.pos1 == pos1]
            if morphs:
                return morphs
            else:
                [m for m in self.morphs if m.pos == pos]

        return [m for m in self.morphs if m.pos == pos]

    def has_str(self, s: str) -> bool:
        # self.morphにsが含まれていればTrue

        for m in self.morphs:
            if m.base == s or m.surface == s:
                return True

        return False


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

    return {c.get_morphs("動詞")[0].base: 
            [chunks[s] for s in c.srcs if chunks[s].has_morph("助詞")] 
            for c in chunks if c.has_morph("動詞")}


def get_sahen(case: dict) -> dict:
    """
    サ変接続名詞 + を(助詞) が動詞に係っているものを抽出
    
    Parameters
    ----------
    case : dict
        get_case()の戻り値 {述語: 述語に係るChunkオブジェクトのリスト}

    Returns
    -------
    sahen : dict
        key : サ変接続名詞 + を + 動詞の基本形
        value : keyの動詞の基本形に係る文節(サ変接続名詞は除く)
    """

    sahen = {}
    for k, v in case.items():
        clause = v
        for i, c in enumerate(v):
            if c.has_morph("名詞", "サ変接続") and c.has_str("を"):
                s_noun = c.not_punctuation() + k
                clause.pop(i)

                sahen[s_noun] = clause

    return sahen


def get_path(chunks: list) -> list:
    """
    名詞を含む文節を葉とした時の、構文木の根に至るパスを返す

    Parameteres
    -----------
    chunks : list
        Chunkオブジェクトのリスト

    Returns
    -------
    result : list
        名詞を含む文節 -> 前の文節のdstの文節 -> ... -> 最終的な係り先の文節
        上記のようなパスのリスト
    """

    result = []
    for chunk in [c for c in chunks if c.has_morph("名詞")]:
        path = [chunk.not_punctuation()]
        c = chunk
        while c.dst > 0:
            c = chunks[c.dst]
            path.append(c.not_punctuation())

        result.append(" -> ".join(path))

    return result


def read_cabocha() -> list:
    with open("./neko.txt.cabocha") as f:
        # 1文をChunkオブジェクトのリストとあるが、扱いづらかったので一旦辞書型に
        chunks = {}
        c = []

        for l in f:
            if l == "EOS\n":
                yield [c[1] for c in sorted(chunks.items(), key=lambda x: x[0])]
                chunks.clear()

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
    import subprocess

    with open("nlp_48.txt", "w") as f:
        # 確認用
        n = int(input(">> "))

        for i, r in enumerate(read_cabocha(), 1):
            path = get_path(r)

            if path:
                for p in path:
                    f.write(p + "\n")

                    if i == n:
                        print(p)
