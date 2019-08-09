# -*- coding: utf-8 -*-

s = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
s = s.translate(str.maketrans({",": "", ".": ""}))
c = [len(w) for w in s.split(" ") if w]
print(c)
