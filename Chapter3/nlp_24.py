# -*- coding: utf-8 -*-

import nlp_22
import re

def get_filename(text: str) -> list:
    pattern = re.compile(r"(?<=\[\[)(?:ファイル:|File:)(.+?)(?=\|)")
    result = pattern.findall(text)

    if result:
        return result
    else:
        return None


if __name__ == "__main__":
    fname = get_filename(nlp_22.uk_text())
    print("\n".join(fname))
