# -*- coding: utf-8 -*-

from pymongo import MongoClient, DESCENDING
from flask import Flask, render_template, request

client = MongoClient()
db = client.artist
collection = db.artist

app = Flask(__name__)

# ルートにアクセスした時の処理
@app.route("/")
def index():
    # index.htmlをレンダリング
    return render_template("index.html")


# get
@app.route("/get", methods=["GET"])
def get():
    # getはargsで値を取れる(postはform)
    key = request.args.get("key", "")
    return search_artist(key)


def search_artist(key):
    # name, aliases, area, tagにマッチするものを取ってくる
    result = collection.find(
            {"$or": [
                {"name": key}, 
                {"aliases.name": key},
                {"area": key},
                {"tags.value": key}
                ]})
    result.sort("rating.value", DESCENDING)
        
    return render_template("result.html", total=result.count(), results=convert(result))


def convert(cursor):
    con = []
    for d in cursor:
        c = {}
        c["name"] = d["name"]
        c["alias"] = ", ".join([a["name"] for a in d["aliases"]] if "aliases" in d else "未登録")
        c["area"] = d.get("area", "未登録")
        c["tag"] = ", ".join([t["value"] for t in d["tags"]] if "tags" in d else "未登録")
        c["rating"] = d.get("rating", {"value": "未登録"})["value"]
        con.append(c)
    
    return con


if __name__ == "__main__":
    app.run(debug=True)
