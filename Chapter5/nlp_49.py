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

    # 追加
    def replace_noun(self, xy: str, omit=False) -> str:
        # morphs内の最初の名詞を任意の文字列に置換
        # omit : 置換した名詞以外は除去 

        s = ""
        for m in self.morphs:
            if m.pos == "名詞":
                # 'XX'みたいになることあるから繰り返さないように
                try:
                    if s[-1] == xy:
                        continue
                except IndexError:
                    pass

                s += xy

                if omit:
                    return s

            elif m.pos != "記号":
                s += m.surface

        return s


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

# 追加
def get_noun_path(chunks: list) -> list:
    """
    文中のすべての名詞句のペアを結ぶ最短係り受けパスを返す

    Parameteres
    -----------
    chunks : list
        Chunkオブジェクトのリスト

    Returns
    -------
    result : list
        名詞句ペアを結ぶ係り受けパスのリスト
        ペアの名詞句はそれぞれ"X"と"Y"で置換

        ・文節iのパス上に文節jのパスがある場合の係り受けパス
            "開始文節 -> 途中の文節 -> ... -> 終了文節"
        ・文節iと文節jが共通の文節kで交わる場合の係り受けパス
            "文節i -> ... -> 文節kの手前 | 文節j -> ... -> 文節kの直前 | 文節k"

    """

    result = []
    paths = []
    nouns = [c for c in chunks if c.has_morph("名詞")]

    if len(chunks) > 1:
        # get_path とほぼ同じ 係り受けパスの抽出
        for chunk in nouns:
            path = [chunk]
            c = chunk
            while c.dst > 0:
                c = chunks[c.dst]
                path.append(c)

            paths.append(path)

        # 文節i、文節jの関係によってパスの表示の仕方を変更
        for i, path in enumerate(paths):
            set_i = set(path)
            
            for p in paths[i+1::]:
                set_j = set(p)

                intersection = set_i & set_j
                
                # 文節i上に文節jが存在する場合
                if intersection == set_j:
                    between = [c.replace_noun("X") if i == 0 else c.not_punctuation()
                            for i, c in enumerate(path) if c not in p]
                    between.append(p[0].replace_noun("Y", omit=True))
                    result.append(" -> ".join(between))
                
                # 文節iと文節jから根へ至る経路上に共通の文節kがある場合
                elif intersection:
                    phrase_i = [c.replace_noun("X") if i == 0 else c.not_punctuation() 
                            for i, c in enumerate(path) if c not in intersection]
                    phrase = [" -> ".join(phrase_i)]

                    phrase_j = [c.replace_noun("Y") if i == 0 else c.not_punctuation() 
                            for i, c in enumerate(p) if c not in intersection]
                    phrase.append(" -> ".join(phrase_j))

                    phrase_k = [c.not_punctuation() for c in p if c in intersection]
                    phrase.append(" -> ".join(phrase_k))

                    result.append(" | ".join(phrase))

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

    with open("nlp_49.txt", "w") as f:
        # 確認用
        n = int(input(">> "))

        for i, r in enumerate(read_cabocha(), 1):
            path = get_noun_path(r)

            if path:
                for p in path:
                    f.write(p + "\n")

                    if i == n:
                        print(p)
