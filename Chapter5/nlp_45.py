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
    
    def get_morphs(self, pos: str) -> list:
        # posに一致する単語の基本形を返す

        return [m.base for m in self.morphs if m.pos == pos]


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
        value : keyの動詞に係る文節内に含まれる格助詞
    """

    # 動詞は最左のものをとる -> get_morphs("動詞")[0]
    # get_morphs()はリストで返ってくるので、二重ループさせて１つのリストに
    return {c.get_morphs("動詞")[0]: 
            [m for s in c.srcs for m in chunks[s].get_morphs("助詞")] 
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
    import subprocess

    with open("nlp_45.txt", "w") as f:
        # 確認用
        n = int(input(">> "))

        for i, r in enumerate(read_cabocha(), 1):
            for c in get_case(r).items():
                if c[1]:
                    f.write(f"{c[0]}\t{' '.join(sorted(c[1]))}\n")

                if i == n:
                    print(f"{c[0]}\t{' '.join(c[1])}")


    # ----------------
    # コマンドでの確認
    # ----------------
    # コーパス中で頻出する述語と格パターンの組み合わせ
    # sort nlp_45.txt | uniq -c | sort -ur > freq_nlp_45.txt
    
    with open("freq_nlp_45.txt", "w") as f:
        p1 = subprocess.Popen(["sort", "nlp_45.txt"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["uniq", "-c"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["sort", "-ur"], stdin=p2.stdout, stdout=f)

    # 「する」「見る」「与える」という動詞の格パターン（コーパス中で出現頻度の高い順に並べよ）
    # grep "^する" nlp_45.txt | sort | uniq -c | sort -ur > suru.txt
    with open("suru.txt", "w") as f:
        p1 = subprocess.Popen(["grep", "^する", "nlp_45.txt"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["sort"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["uniq", "-c"], stdin=p2.stdout, stdout=subprocess.PIPE)
        p4 = subprocess.Popen(["sort", "-ur"], stdin=p3.stdout, stdout=f)

    # grep "^見る" nlp_45.txt | sort | uniq -c | sort -ur > miru.txt
    with open("miru.txt", "w") as f:
        p1 = subprocess.Popen(["grep", "^見る", "nlp_45.txt"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["sort"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["uniq", "-c"], stdin=p2.stdout, stdout=subprocess.PIPE)
        p4 = subprocess.Popen(["sort", "-ur"], stdin=p3.stdout, stdout=f)
    
    # grep "^与える" nlp_45.txt | sort | uniq -c | sort -ur > ataeru.txt
    with open("ataeru.txt", "w") as f:
        p1 = subprocess.Popen(["grep", "^与える", "nlp_45.txt"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["sort"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["uniq", "-c"], stdin=p2.stdout, stdout=subprocess.PIPE)
        p4 = subprocess.Popen(["sort", "-ur"], stdin=p3.stdout, stdout=f)
