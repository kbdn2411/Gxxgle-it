from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
from bs4 import BeautifulSoup
import random
import re

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
# 亂輸入判斷
# ======================
def is_messy_input(q: str) -> bool:
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
# 政治判斷（完整強化版）
# ======================
def is_politics(q: str) -> bool:
    qn = re.sub(r"\s+", "", q)

    keywords = [
        "政府", "選舉", "總統", "立委", "市長", "縣長",
        "政策", "政治", "政黨", "內閣",
        "立法院", "行政院",
        "民進黨", "國民黨", "民眾黨",
        "柯文哲", "賴清德", "侯友宜", "韓國瑜",
        "蔡英文", "陳水扁", "馬英九",
        "柯p", "阿北", "小英", "賴神", "韓導",
        "新聞", "訪美", "外交", "川普", "拜登", "中國", "美國"
    ]

    return any(k in qn for k in keywords)

# ======================
# AI 核心（乾淨嗆版）
# ======================
def generate_answer(q, ptt, reddit):

    # 1️⃣ 亂輸入
    if is_messy_input(q):
        return "你這輸入是認真的嗎？先把字打好再來查。"

    # 2️⃣ 沒資料
    base = ptt + reddit
    if not base:
        return "查不到東西就代表這題本來就沒什麼人在認真討論。"

    # 3️⃣ 判斷類型
    if is_politics(q):
        templates = [
            "這題就是立場問題，不是知識問題，沒有標準答案。",
            "政治討論本來就只會互相打臉，不會有共識。",
            "不同陣營講法完全相反，你看到的是對立不是資訊。",
            "這種問題本質就是分裂，不存在客觀解。",
            "結論很簡單：這題沒有結論。"
        ]
    else:
        templates = [
            "這題沒有唯一答案，本來就會互相矛盾。",
            "資訊來源不同，所以看起來才會混亂。",
            "這種問題再查一次結果也不會改變。",
            "你看到的是不同版本，不是錯誤。",
            "本質就是資訊分散，沒有統一解。"
        ]

    # 4️⃣ 加強嗆句
    roast = [
        "不用再查了，結果不會變。",
        "你會覺得亂只是因為本來就沒答案。",
        "再看一次也不會更清楚。",
        "這題本來就沒有標準解。",
        "你現在查只是浪費時間。"
    ]

    return f"{random.choice(templates)} {random.choice(roast)}"

# ======================
# UI
# ======================
@app.get("/")
def home():
    return FileResponse("static/index.html")

# ======================
# API（乾淨輸出）
# ======================
@app.get("/search")
def search(q: str):

    ptt = get_ptt(q)
    reddit = get_reddit(q)

    return {
        "answer": generate_answer(q, ptt, reddit)
    }
