# -*- coding: utf-8 -*-

def cipher(string):
    return "".join([chr(219 - ord(s)) if s.islower() else s for s in string])

if __name__ == "__main__":
    s = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
    print(f"input: \n{s}\n")
    print(f"encryption: \n{cipher(s)}\n")
    print(f"decryption: \n{cipher(cipher(s))}")
