# -*- coding: utf-8 -*-

import nlp_22
import nlp_25
import nlp_26
import nlp_27
import re

def exclude_markup() -> dict:
    inf = nlp_25.stdinf(nlp_22.uk_text())
    d = nlp_26.exclude_emphasis(inf)
    d = nlp_27.exclude_link(d)

    # {{lang|**|++}} の除去
    pattern = re.compile(r"""
            \{\{
            lang\|.+?\|
            (.+?)
            \}\}
            """, re.VERBOSE)

    d =  {k: pattern.sub(r"\1", v) for k, v in d.items()}

    # <ref> <br/> タグの除去
    pattern = re.compile(r"<\/?(?:ref|br)[^>]*?>")
    d =  {k: pattern.sub("", v) for k, v in d.items()}

    # 外部リンクの除去 [http://*** xxx]
    pattern = re.compile(r"\[http(?:[^\s]*?\s)?((?<=\s).+?)\]")
    d =  {k: pattern.sub(r"\1", v) for k, v in d.items()}

    # 外部リンクの除去 [http://***]
    pattern = re.compile(r"\[http.+\]")
    d =  {k: pattern.sub("", v) for k, v in d.items()}

    # ファイルの除去
    pattern = re.compile(r"\[\[(?:ファイル:|File:)(.+?)\|.*?\]\]")
    d =  {k: pattern.sub(r"\1", v) for k, v in d.items()}

    # 箇条書きの除去
    pattern = re.compile(r"\*{1,2}")
    d =  {k: pattern.sub("", v) for k, v in d.items()}

    return d


if __name__ == "__main__":
    inf_dic = nlp_25.stdinf(nlp_22.uk_text())
    inf_dic = nlp_26.exclude_emphasis(inf_dic)
    inf_dic = nlp_27.exclude_link(inf_dic)
    inf_dic = exclude_markup(inf_dic)

    print("\n".join([f"{k}: {v}" for k, v in inf_dic.items()]))
