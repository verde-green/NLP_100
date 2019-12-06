# -*- coding: utf-8 -*-

import os
import subprocess
from xml.etree import ElementTree as ET

def stanford():
    # classpathがうまく指定できなかった
    # /usr/local/lib/stanford-corenlp-full-2018-10-05/で直接xmlファイル生成

    fname = "nlp.txt"
    if not os.path.isfile(fname + ".xml"):
        cmd = "java -Xmx3g -cp '/usr/local/lib/stanford-corenlp-full-2018-10-05/*' " \
                "edu.stanford.nlp.pipeline.StanfordCoreNLP " \
                "-annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref " \
                "-file" + fname
        subprocess.run(cmd.split(" "), check=True)


if __name__ == "__main__":
    root = ET.parse("nlp.txt.xml")
    for w in root.iter("word"):
        print(w.text)
