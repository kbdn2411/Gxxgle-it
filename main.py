from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
from bs4 import BeautifulSoup
import random

app = FastAPI()

# ======================
# Reddit
# ======================
def get_reddit(q):
    url = f"https://www.reddit.com/search.json?q={q}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()
        return [c["data"]["title"] for c in data["data"]["children"]][:5]
    except:
        return []

# ======================
# PTT
# ======================
def get_ptt(q):
    url = f"https://www.ptt.cc/bbs/Gossiping/search?q={q}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, cookies={"over18": "1"}, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        return [t.text.strip() for t in soup.select(".title a")][:5]
    except:
        return []

# ======================
# 政治關鍵字
# ======================
politics_keywords = [
    "政府", "選舉", "總統", "立委", "政策",
    "台灣", "柯文哲", "賴清德", "侯友宜",
    "韓國瑜", "蔡英文", "陳水扁", "阿扁"
]

def is_politics(q):
    return any(k in q for k in politics_keywords)

# ======================
# AI 回答層（極簡版）
# ======================
def generate_answer(q, ptt, reddit):

    base = ptt + reddit

    # ======================
    # 沒資料
    # ======================
    if not base:
        return "這種查詢目前沒人在乎，你查到這裡其實也不會多一個答案。"

    # ======================
    # 🔥 錯字嗆人判斷（新增）
    # ======================
    raw = q.strip()

    # 簡單判斷：太亂 / 太短 / 含奇怪符號
    messy = (
        len(raw) <= 1 or
        raw.count(" ") > 5 or
        any(c in raw for c in ["@@", "##", "$$", "？？？"])
    )

    if messy:
        return "你這輸入是認真的嗎？先把字打好再來查。"

    # ======================
    # 一般模板
    # ======================
    general_templates = [
        "這題其實早就有人問過了。",
        "資料本來就混在一起，沒有標準答案。",
        "這種問題再查一次結果也不會變。",
        "各種來源說法不同，本來就沒有結論。",
        "這類問題就是資訊分歧。"
    ]

    # ======================
    # 政治模板
    # ======================
    politics_templates = [
        "政治問題本來就沒有共識。",
        "不同立場各說各話。",
        "這種議題本質就是對立，不會有答案。",
        "網路討論最後都會變成立場問題。",
        "政治議題沒有單一結論。"
    ]

    templates = politics_templates if is_politics(q) else general_templates

 

import re

def is_messy_input(q: str) -> bool:
    q = q.strip()

    # 1️⃣ 太短
    if len(q) <= 1:
        return True

    # 2️⃣ 大量非文字（像亂碼 / 注音鍵盤亂按）
    if re.fullmatch(r"[^\u4e00-\u9fffA-Za-z0-9]+", q):
        return True

    # 3️⃣ 重複無意義字元（例如：ㄅㄅㄅㄅ / asdfasdf）
    if len(set(q)) <= 2 and len(q) > 3:
        return True

    # 4️⃣ 英文鍵盤亂打常見型
    gibberish_patterns = [
        "asdf", "jkl", "qwe", "zxc", "ㄅㄆㄇ", "ㄆㄇㄈ"
    ]
    if any(p in q.lower() for p in gibberish_patterns):
        return True

    return False
   
# ======================
# UI
# ======================
@app.get("/")
def home():
    return FileResponse("static/index.html")

# ======================
# API
# ======================
@app.get("/search")
def search(q: str):

    ptt = get_ptt(q)
    reddit = get_reddit(q)

    return {
        "query": q,
        "answer": generate_answer(q, ptt, reddit)
    }
