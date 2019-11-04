# -*- coding: utf-8 -*-

import subprocess

if __name__ == "__main__":
    with open("./col1.txt") as col1, \
            open("./col2.txt") as col2:
                data1 = [c.replace("\n", "") for c in col1.readlines()]

                line = [d1 + "\t" + d2 for d1, d2 in zip(data1, col2.readlines())]
            
    with open("merge.txt", "w") as f:
        f.writelines(line)

    # check
    cmd = "paste ./col1.txt ./col2.txt"
    paste = subprocess.check_output(cmd.split(" ")).decode("utf-8")
    
    if "".join(line) == paste:
        print("paste command check ok")
