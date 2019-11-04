# -*- coding: utf-8 -*-

import subprocess

with open("./merge.txt") as f:
    line = f.readlines()

n = int(input("末尾から表示する行数: "))
print("\nprogram\n")
print("".join(line[-n::]))
print("-"*10)

# check
print("tail command\n")

cmd = f"tail -n {n} ./merge.txt"
tail = subprocess.check_output(cmd.split(" ")).decode("utf-8")
print(tail)
print("-"*10)

if "".join(line[-n::]) == tail:
    print("check ok")
