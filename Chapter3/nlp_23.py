# -*- coding: utf-8 -*-

import nlp_22
import re

def section(text: str) -> str:
    pattern = re.compile(r"(={2,})\s*(.+?)\s*={2,}")
    result = pattern.findall(text)

    if result:
        # = の数をレベルに置き換え
        return [(len(r[0]) - 1, r[1]) for r in result]
    else:
        return None


if __name__ == "__main__":
    sec = section(nlp_22.uk_text())
    print("\n".join([f"{s[1]} {s[0]}" for s in sec]))
