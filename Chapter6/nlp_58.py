# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET

root = ET.parse("nlp.txt.xml")

for dependencies in root.iterfind("./document/sentences/sentence/dependencies[@type='collapsed-dependencies']"):
    
    # {述語のidx: {"pred": 述語, "subj": 主語, "obj": 目的語}}
    three_tuples = {}
    
    for dep in dependencies.iter("dep"):
        d_type = dep.get("type")
        g_idx = dep.find("governor").get("idx")

        if d_type == "nsubj":
            three_tuples.setdefault(g_idx, {})
            three_tuples[g_idx].setdefault("pred", dep.findtext("governor"))
            three_tuples[g_idx]["subj"] = dep.findtext("dependent")

        elif d_type == "dobj":
            three_tuples.setdefault(g_idx, {})
            three_tuples[g_idx].setdefault("pred", dep.findtext("governor"))
            three_tuples[g_idx]["obj"] = dep.findtext("dependent")

    for v in three_tuples.values():
        if len(v) == 3:
            print(f"{v['subj']}\t{v['pred']}\t{v['obj']}")
