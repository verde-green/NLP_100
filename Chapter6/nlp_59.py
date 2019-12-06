# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
import re

# Stanford Core NLPのS式の構造は (タグ (タグ 単語) (...) ...) 
pattern = re.compile(r"\((.+?)\s(.+)$")

def proof(text: str) -> str:
    t = re.sub(r"-LRB-\s(.+?)\s-RRB-", r"(\1)", text)
    t = re.sub(r"`\s(.+?)\s'", r"`\1'", t)
    return re.sub(r"(\s)(?=[.,;:!?])", "", t)


def resolve_tag(parse: str, np: list) -> str:
    """
    S式で表されたparseから名詞句(NP)のみ抽出して、npに入れる

    Parameters
    ----------
    parse : str
        S式
    np : list
        名詞句を保持するリスト

    Returns
    -------
    result : str
        構文木の終端記号
        単語
    """

    search = pattern.search(parse)
    tag = search.group(1)
    
    s = ""
    depth = 0
    words = []
    for c in search.group(2):
        if c == "(":
            s += c
            depth += 1

        elif c == ")":
            s += c
            depth -= 1
            
            # ()の組みができた
            if depth == 0:
                # 再帰させて終端記号を全部取り出す
                words.append(resolve_tag(s, np))
                s = ""

            elif depth == -1 and s[:-1]:
                # (タグ 単語)の形式の場合、search.group(2): 単語) なので最後まで読むとdepth = -1
                # 終端記号の取り出し
                words.append(s[:-1])
                break

        else:
            s += c
    
    result = " ".join(words)
    
    # 名詞句のみリストに保持
    if tag == "NP":
        np.append(proof(result))

    return result


root = ET.parse("nlp.txt.xml")

np = []
for parse in root.iter("parse"):
    resolve_tag(parse.text, np)

print(*np, sep="\n")
