# -*- coding: utf-8 -*-

import subprocess

with open("hightemp.txt") as f:
    line = [l.split("\t") for l in f.readlines()]

line.sort(key=lambda x: x[2], reverse=True)
print("".join(["\t".join(l) for l in line]))

# sort command
cmd = 'sort --key=3,3 --numeric-sort --reverse hightemp.txt'
result = subprocess.check_output(cmd.split(" ")).decode("utf-8")
print("-"*5)
print("sort command\n")
print(result)
