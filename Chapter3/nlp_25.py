# -*- coding: utf-8 -*-

import nlp_22
import re

def stdinf(text: str) -> dict:
    pattern = re.compile(r"\{\{基礎情報(.+?)^\}\}$", re.MULTILINE + re.DOTALL)
    inf = pattern.search(text)

    if inf:
        pattern = re.compile(r"""
            ^\|
            (.+?)
            \s=\s
            (.+?)
            (?=(\n\|)|(\n$))
            """, re.VERBOSE + re.MULTILINE + re.DOTALL)
        return {i[0]: i[1] for i in pattern.findall(inf.group(0))}
    else:
        return None


if __name__ == "__main__":
    inf = stdinf(nlp_22.uk_text())
    print("\n".join([f"{k}: {v}" for k, v in inf.items()]))

