#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: main.py
# DATE: 2021/12/08
# TIME: 13:19:23

# DESCRIPTION: main.py

from os import write
import requests
from bs4 import BeautifulSoup
from kinder import kinder

mainUrl = ""
kinderUrl = ""
pageStrFirst = "_0_0_11_0_1_"
pageStrEnd = "_0_0_"

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"
    }

targetKinder = [
    "纪实文学"
]

resultPageHead = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<style>
    li {
        list-style: none;
        border-bottom: 1px solid #000;
    }
    .pic {
        float: left;
        width: 200px;
    }
    .book {
        width: 800px;
    }
    .clear {
        clear: both;
    }
</style>
<body>
    <ul>
"""

resultPageEnd = """
    </ul>
</body>
</html>
"""


def getKey(value):
    ### get books kinder key
    for key,val in kinder.items():
        if value == val:
            return key
    
    return 0


def main():
    ### main
    s = requests.session()
    r = s.get(mainUrl)
    for x in targetKinder:
        with open(x + ".html", "w", encoding="utf-8") as f:
            f.write(resultPageHead)
            key = getKey(x)
            kUrl = kinderUrl + str(key)
            print(kUrl)
            r = s.get(kUrl)
            soup = BeautifulSoup(r.text, "html5lib")
            # 当前分类获取总页码
            totalPageNum = soup.select_one("#container > div > div.listLeft > div.pagination > div > div > em:nth-child(1) > b").text

            for p in range(1, int(totalPageNum) + 1):
                pUrl = kinderUrl + str(key) + pageStrFirst + str(p) + pageStrEnd
                print(pUrl)
                r = s.get(pUrl)
                soup = BeautifulSoup(r.text, "html5lib")
                activeIcon = soup.select("div.activeIcon > a")
                for y in activeIcon:
                    bookName = y.parent.find_parent("li").find("h2").text
                    bookUrl = y.parent.find_parent("li").find("h2").find("a")["href"]
                    sellPrice = y.parent.find_parent("li").find (class_="sellPrice").text
                    bookIntro = y.parent.find_parent("li").find (class_="recoLagu").text
                    otherInfo = y.parent.find_parent("li").find (class_="otherInfor").text
                    pic = y.parent.find_parent("li").find("img")["data-original"]
                    booksHTML = """
                    <li>
                    <div class="pic"><img src="{pic}" alt="" srcset=""></div>
                    <div class="book">
                    <div class="name"><a href="{bookUrl}" target="_blank">{bookName}</a></div>
                    <div class="info">{otherInfo}</div>
                    <div class="price">{sellPrice}</div>
                    <div class="bookintro">{bookIntro}</div>
                    </div>
                    <div class="clear"></div>
                    </li>
                    """.format(
                        pic=pic,
                        bookUrl=mainUrl + bookUrl,
                        bookName=bookName,
                        sellPrice=sellPrice,
                        bookIntro=bookIntro,
                        otherInfo=otherInfo
                    )
                    f.write(booksHTML)
            f.write(resultPageEnd)
            f.close()

if __name__ == "__main__":
    main()