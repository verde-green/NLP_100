# -*- coding: utf-8 -*-

import nlp_42
from graphviz import Digraph

G = Digraph(filename="nlp_44")

for i, r in enumerate(nlp_42.read_cabocha()):
    if i == 7:
        # nodeとedgeの追加
        for m in r:
            G.node(m.not_punctuation())
            
            if m.dst > 0:
                G.edge(m.not_punctuation(), r[m.dst].not_punctuation())

        break

G.view()
