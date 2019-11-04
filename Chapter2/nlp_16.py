# -*- coding: utf-8 -*-

import math
import sys
import subprocess

def divide(n: int):
    with open("./hightemp.txt") as f:
        line = f.readlines()

    u = math.ceil(len(line) / n)
    d = [math.ceil(len(line) / n)]*n

    start = [sum(d[:i]) for i in range(n)]
    stop = [sum(d[:i]) for i in range(1, n + 1)]
    data = [line[i:j] for i, j in zip(start, stop)]
    
    subprocess.call(["mkdir", "divided_file"])
    for i, d in enumerate(data):
        with open(f"divided_file/divide_{i}.txt", "w") as f:
            f.writelines(d)

    check(n, u)


def check(n: int, u: int):
    # 0 -> a ... 25 -> z
    num2alp = lambda c: chr(c + 97)

    subprocess.call(["mkdir", "split_file"])
    
    # split コマンドの実行 
    # macのsplitコマンドに--numeric-suffixesがなかった
    cmd = f"split -l {u} -a 1 hightemp.txt split_file/split_"
    subprocess.call(cmd.split(" "))
    
    for i in range(n):
        with open(f"divided_file/divide_{i}.txt") as f:
            d = f.readlines()
        with open(f"split_file/split_{num2alp(i)}") as f:
            s = f.readlines()

        if d != s:
            print("The result is different from split command...")
            return

    print("split command check OK!")


if __name__ == '__main__':
    # 分割ファイルを保存するかどうかをコマンドライン引数で管理
    # n : 分割ファイルを保存しない
    args = sys.argv

    n = int(input("hightemp.txt 分割数: "))
    divide(n)
    
    if len(args) > 1:
        if args[1] == "n":
            cmd = "rm -rf divided_file split_file"
            subprocess.call(cmd.split(" "))
