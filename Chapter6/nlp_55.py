# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET

root = ET.parse("nlp.txt.xml")

"""
for token in root.iter("token"):
    if token.findtext("NER") == "PERSON":
        print(token.findtext("word"))
"""

# iterfind(match)でタグ名orパスがmatchにマッチするすべての要素のイテレータが返ってくる
for token in root.iterfind("./document/sentences/sentence/tokens/token[NER='PERSON']"):
    print(token.findtext("word"))
