# -*- coding: utf-8 -*-
import random

def typoglycemia(text):
    result = []
    
    for w in [word for word in text.split(" ") if word]:
        if len(w) > 4:
            result.append(w[0] + "".join(random.sample(w[1:-1:], len(w) - 2)) + w[-1])
        else:
            result.append(w)

    return " ".join(result)

if __name__ == "__main__":
    text = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
    print(f"input:\n{text}")
    print(f"typoglycemia:\n{typoglycemia(text)}")
