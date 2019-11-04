# -*- coding: utf-8 -*-

import nlp_28
import requests

def get_flag_url(inf_dic: dict):
    url = "https://mediawiki.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles=File:" + inf_dic["国旗画像"]
    
    data = requests.get(url).json()
    return data["query"]["pages"]["-1"]["imageinfo"][0]["url"]


if __name__ == "__main__":
    print(get_flag_url(nlp_28.exclude_markup()))
