# -*- coding: utf-8 -*-
import subprocess

with open("hightemp.txt") as f:
    line = f.readlines()

col = list(set([l.split("\t")[0] for l in line]))
[print(c) for c in col]

# check
# sort col1.txt | uniq 的なことをしたかった
cmd = "sort col1.txt"
p1 = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
p2 = subprocess.Popen(["uniq"], stdin=p1.stdout, stdout=subprocess.PIPE)
result = p2.communicate()[0].decode("utf-8")
print("-"*5)
print("uniq command\n")
print(result)

col.sort()
# split後に空の文字列を除くため
if col == sorted([r for r in result.split("\n") if r]):
    print("uniq command check ok!")
else:
    print("the result different from uniq command...")
