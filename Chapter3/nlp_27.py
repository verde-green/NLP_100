# -*- coding: utf-8 -*-

import nlp_22
import nlp_25
import nlp_26
import re

def exclude_link(inf_dic: dict) -> dict:
    pattern = re.compile(r"""
            \[\[
            (?:[^|]+?\|)?
            ([^|]+?)
            \]\]
            """, re.VERBOSE)

    return {k: pattern.sub(r"\1", v) for k, v in inf_dic.items()}


if __name__ == "__main__":
    inf_dic = nlp_25.stdinf(nlp_22.uk_text())
    inf_dic = nlp_26.exclude_emphasis(inf_dic)
    inf_dic = exclude_link(inf_dic)

    print("\n".join([f"{k}: {v}" for k, v in inf_dic.items()]))
