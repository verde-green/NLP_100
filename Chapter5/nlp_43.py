# -*- coding: utf-8 -*-

import nlp_42

for i, r in enumerate(nlp_42.read_cabocha()):
    if i < 10:
        relation = [[m.not_punctuation(), r[m.dst].not_punctuation()] for m in r 
            if m.dst >= 0 
            and "名詞" in [mm.pos for mm in m.morphs] 
            and "動詞" in [rm.pos for rm in r[m.dst].morphs]]

        for rel in relation:
            if rel[0] and rel[1]:
                print(f"{rel[0]}\t{rel[1]}")
