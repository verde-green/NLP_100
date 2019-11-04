# -*- coding: utf-8 -*-

import subprocess

with open("./merge.txt") as f:
    line = f.readlines()

n = int(input("先頭から表示する行数: "))
print("\nprogram\n")
print("".join(line[:n:]))
print("-"*10)

# check
print("head command\n")

cmd = f"head -n {n} ./merge.txt"
head = subprocess.check_output(cmd.split(" ")).decode("utf-8")
print(head)
print("-"*10)

if "".join(line[:n:]) == head:
    print("check ok")
