# -*- coding: utf-8 -*-

import subprocess
import collections

with open("hightemp.txt") as f:
    col = [l.split("\t")[0] for l in f.readlines()]

c = collections.Counter(col)
[print(f"{m[0]}: {m[1]}") for m in c.most_common()]

# check
# sort col1.txt | uniq -c | sort -r
p1 = subprocess.Popen(["sort", "col1.txt"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["uniq", "-c"], stdin=p1.stdout, stdout=subprocess.PIPE)
p3 = subprocess.Popen(["sort", "-r"], stdin=p2.stdout, stdout=subprocess.PIPE)
result = p3.communicate()[0].decode("utf-8")
print("-"*5)
print("sort, uinq command\n")
print(result)
