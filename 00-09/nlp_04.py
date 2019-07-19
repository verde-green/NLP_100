# -*- coding: utf-8 -*-

s = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can.".replace(".", "")
one = [1, 5, 6, 7, 8, 9, 15, 16, 19]
d = {w[0] if i in one else w[:2:] : i for i, w in enumerate(s.split(" "), 1)}
print(d)
