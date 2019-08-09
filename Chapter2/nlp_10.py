# -*- coding: utf-8 -*-

# subprocess: pythonでsh実行
import subprocess

if __name__ == "__main__":
    with open("./hightemp.txt") as f:
        print(f"python: {len(f.readlines())}")
    
    # bytes型で返ってきた
    # 自分の環境だと空白がいっぱいついてた
    result = subprocess.check_output(["wc", "-l", "./hightemp.txt"]).decode()
    print(f"sh: {result[6::]}")
