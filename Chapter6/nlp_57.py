# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
from graphviz import Digraph

def make_graph(edges: list) -> Digraph:
    """
    エッジのリストから有向グラフを生成

    Parameters
    ----------
    edges : list
        エッジのリスト。エッジはタプルで構成
        [(((識別子1, ラベル1), (識別子2, ラベル2)), (...), ...)]

    Reteruns
    --------
    G : Digraph
        有向グラフのオブジェクト
    """

    # nlp_57.pngでグラフが保存される
    G = Digraph(format="png")

    for edge in edges:
        n1 = edge[0][0]
        n2 = edge[1][0]
        
        # ノード追加
        # idxの値が異なれば、別なノードとする
        G.node(n1, label=edge[0][1])
        G.node(n2, label=edge[1][1])

        # エッジの追加
        G.edge(n1, n2)
    
    return G


if __name__ == "__main__":
    root = ET.parse("nlp.txt.xml")

    for dependencies in root.iterfind("./document/sentences/sentence/dependencies[@type='collapsed-dependencies']"):
        edges = []

        for dep in dependencies.iter("dep"):
            # print(f"{dep.find('governor').get('idx')} {dep.findtext('governor')} -> {dep.find('dependent').get('idx')} {dep.findtext('dependent')}")
            
            # 句読点に係るものはエッジに含めない
            if dep.get("type") == "punct":
                continue

            else:
                edges.append((
                    (dep.find("governor").get("idx"), dep.findtext("governor")),
                    (dep.find("dependent").get("idx"), dep.findtext("dependent"))
                    ))
        
        G = make_graph(edges)
        # G.view()
        G.render("nlp_57")

        # とりあえず１文目だけ生成
        break
