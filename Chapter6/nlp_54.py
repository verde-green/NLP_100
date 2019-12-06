# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET

root = ET.parse("nlp.txt.xml")
for token in root.iter("token"):
    print(f"{token.findtext('word')}\t{token.findtext('lemma')}\t{token.findtext('POS')}")
