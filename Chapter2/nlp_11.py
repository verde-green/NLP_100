# -*- coding: utf-8 -*-

import subprocess

if __name__ == "__main__":
    with open("./hightemp.txt") as f:
        print("python:")
        [print(l.replace("\t", " ")) for l in f.readlines()]

    print("sh:")
    print(subprocess.check_output("cat hightemp.txt | tr '\t', ' '", shell=True).decode())
