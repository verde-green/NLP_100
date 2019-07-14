# -*- coding: utf-8 -*-

s = ["パトカー", "タクシー"]
r = [p+t for p, t in zip(s[0], s[1])]
print("".join(r))
