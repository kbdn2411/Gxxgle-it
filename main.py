from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
from bs4 import BeautifulSoup
import random
import re

app = FastAPI()

# ======================
# Reddit（內部參考用）
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
# PTT（內部參考用）
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
# 政治判斷（語意版）
# ======================
def is_politics(q: str) -> bool:
    qn = re.sub(r"\s+", "", q)

    keywords = [
        "政府", "選舉", "總統", "立委", "政策",
        "台灣", "柯文哲", "賴清德", "侯友宜",
        "韓國瑜", "蔡英文", "陳水扁", "阿扁",
        "民進黨", "國民黨", "民眾黨",
        "立法院", "行政院"
    ]

    return any(k in qn for k in keywords)

# ======================
# 亂輸入判斷（注音/亂碼）
# ======================
def is_messy(q: str) -> bool:
    q = q.strip()

    if len(q) <= 1:
        return True

    if re.fullmatch(r"[^\u4e00-\u9fffA-Za-z0-9]+", q):
        return True

    if len(set(q)) <= 2 and len(q) > 3:
        return True

    gibberish = ["asdf", "qwe", "zxc", "jkl", "ㄅㄆㄇ"]
    if any(g in q.lower() for g in gibberish):
        return True

    return False

# ======================
# AI 回答（純一句話）
# ======================
def generate_answer(q, ptt, reddit):

    # ❗亂輸入直接嗆
    if is_messy(q):
        return "你這輸入是認真的嗎？先把字打好再來查。"

    # ======================
    # 一般模板（你要的回來了）
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
        "這種政治問題本來就沒有標準答案，各方立場不同。",
        "政治議題通常不會有共識，只會有立場差異。",
        "這類問題在網路上永遠吵不完，也不會有結論。",
        "政治本質就是分歧資訊，不存在單一正解。"
    ]

    # ❗沒有資料才嗆這個（修正你之前 base 問題）
    base = ptt + reddit
    if not base:
        return "這種查詢目前沒人在乎，你查到這裡其實也不會多一個答案。"

    templates = politics_templates if is_politics(q) else general_templates

    return random.choice(templates)

# ======================
# UI
# ======================
@app.get("/")
def home():
    return FileResponse("static/index.html")

# ======================
# API（只回一句話）
# ======================
@app.get("/search")
def search(q: str):

    ptt = get_ptt(q)
    reddit = get_reddit(q)

    return {
        "answer": generate_answer(q, ptt, reddit)
    }
