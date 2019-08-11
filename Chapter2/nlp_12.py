# -*- coding: utf-8 -*-
# hightemp.txtの1列目 -> col1.txt
# hightemp.txtの2列目 -> col2.txt

import subprocess

if __name__ == "__main__":
    with open("./hightemp.txt") as f:
        line = [l.split("\t") for l in f.readlines()]
        col1 = [l[0] + "\n" for l in line]
        col2 = [l[1] + "\n" for l in line]

    with open("./col1.txt", "w") as f:
        f.writelines(col1)

    with open("./col2.txt", "w") as f:
        f.writelines(col2)

    cut = [
            subprocess.check_output("cut -f 1 -d '\t' ./hightemp.txt", shell=True).decode(),
            subprocess.check_output("cut -f 2 -d '\t' ./hightemp.txt", shell=True).decode()
          ]

    print("cutコマンドとの比較")
    if "".join(col1) == cut[0]:
        print("col1: ok")
    else:
        print("col1: x")
    if "".join(col2) == cut[1]:
        print("col2: ok")
    else:
        print("col2: x")
