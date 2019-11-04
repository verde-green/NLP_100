# -*- coding: utf-8 -*-

import nlp_22
import nlp_25
import re

def exclude_emphasis(inf_dic: dict) -> dict:
    return {k: re.sub(r"\'{2,5}(.+?)\'{2,5}", r"\1", v) for k, v in inf_dic.items()}


if __name__ == "__main__":
    inf_dic = nlp_25.stdinf(nlp_22.uk_text())
    inf_dic = exclude_emphasis(inf_dic)

    print("\n".join([f"{k}: {v}" for k, v in inf_dic.items()]))
