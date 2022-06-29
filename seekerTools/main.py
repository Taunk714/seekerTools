# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import re
import requests  # 导入requests包
from bs4 import BeautifulSoup
import base64


# from bs4 import BeautifulSoup
from typing import Optional

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

@app.get("/dou")
def read_root(url: Optional[str] = None):
    print(url)
    ret_data = fetch_doulist(url)
    print("out function")
    return json.dumps({"data": ret_data})


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def fetch_doulist(url):
    headers = {
        # 'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }

    strhtml = requests.get(url, headers=headers)  # Get方式获取网页数据

    # 创建一个BeautifulSoup解析对象
    soup = BeautifulSoup(strhtml.text, "html.parser", from_encoding="utf-8")
    doulist_name = soup.select('#content > div > div.article > div.doulist-item > div.mod > div.bd.doulist-subject')
    doulist = []
    for item in doulist_name:
        img = item.img.get('src')
        title = item.select('div > div.title')[0].text.strip()
        # request_img(img, title)
        result = {
            'from': item.div.text.strip()[3:],
            'title': title,
            'cover': img,
            # 'cover_data': base64.b64encode(request_img(img, title)),
            'link': item.a.get("href"),
            'author': item.select('div > div.abstract')[0].text.strip().split("\n")[0]
        }
        doulist.append(result)
    return doulist


def request_img(img_url, title):
    strhtml = requests.get(img_url)  # Get方式获取网页数据
    # with open(title.replace(' ', '_') +'.jpg', 'wb') as f:
    #     f.write(strhtml.content)
    #     f.close()
    # print(strhtml)
    # print("************************************")
    # print(base64.b64encode(strhtml.content))
    # print("===================================")
    # print(base64.b64encode(strhtml.content).decode("utf8"))
    return strhtml.content


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    url = "https://www.douban.com/doulist/150946850/"
    url2 = "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2620921357.jpg"
    fetch_doulist(url)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
