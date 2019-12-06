# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
import re

def proof(sentence: str) -> str:
    # 先頭文字のみ大文字に変換
    # capitalize()は先頭以外を小文字にして返す
    text = sentence[0].upper() + sentence[1:]

    # -LRB- word -RRB- -> (word)
    text = re.sub(r"-LRB-\s(.+?)\s-RRB-", r"(\1)", text)
    
    # `` word '' -> ``word''
    text = re.sub(r"`\s(.+?)\s'", r"`\1'", text)
    
    return re.sub(r"(\s)(?=[.,;:!?])", "", text)


if __name__ == "__main__":
    root = ET.parse("nlp.txt.xml")

    # {参照表現のsentence_id: (代表参照表現, (開始token_id, 終了token_id))}
    coreference = {}
    mentions = {}

    for mention in root.iter("mention"):
        # 代表参照表現かどうか @representative="true"
        if mention.attrib:
            # 参照表現の情報があれば辞書に格納
            if mentions:
                for k, v in mentions.items():
                    coreference[k] = (rep, v)
            
                mentions = {}

            rep = mention.findtext("text")
    
        else:
            mentions[mention.findtext("sentence")] = (mention.findtext("start"), mention.findtext("end"))


    words = []
    isMention = False
    for sentence in root.iter("sentence"):
        sentence_id = sentence.get("id")

        if not sentence_id:
            break

        for token in sentence.iter("token"):
            token_id = token.get("id")
        
            # 参照表現の開始位置かどうか
            if sentence_id in coreference and token_id == coreference[sentence_id][1][0]: 
                isMention = True
                mention = token.findtext("word")
        
            elif isMention:
                # 代表参照表現に置換
                if token_id == coreference[sentence_id][1][1]:
                    words.append(coreference[sentence_id][0] + f" ({mention})")
                    words.append(token.findtext("word"))
                    isMention = False

                else:
                    mention += " " + token.findtext("word")
        
            else:
                words.append(token.findtext("word"))

        print(proof(" ".join(words)))
        words.clear()
