# -*- coding: utf-8 -*-

import gzip
import json
import re

def uk_text() -> str:
    with gzip.open("jawiki-country.json.gz", "rt") as f:
        for l in f:
            data = json.loads(l)
            if data["title"] == "イギリス":
                return data["text"]

def category(text: str):
    pattern = re.compile(r"(?<=\[\[Category:)(.+?)(?:\|.+)?(?=\]\])")
    result = pattern.findall(text)
    
    if result:
        return result
    else:
        return None

if __name__ == "__main__":
    [print(c) for c in category(uk_text())]
