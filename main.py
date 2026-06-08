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
# 正規化
# ======================
def normalize(q: str) -> str:
    return re.sub(r"\s+", "", q).lower()

# ======================
# 語意政治判斷（升級版）
# ======================
def is_politics(q: str) -> bool:
    qn = normalize(q)

    keywords = [
        "政府", "選舉", "總統", "立委", "政策",
        "台灣", "柯文哲", "賴清德", "侯友宜",
        "韓國瑜", "蔡英文", "陳水扁", "阿扁",
        "民進黨", "國民黨", "民眾黨",
        "投票", "大選", "立法院", "行政院"
    ]

    if any(k in qn for k in keywords):
        return True

    # 拆字容錯
    if any(all(c in qn for c in k) for k in ["韓國瑜", "蔡英文", "柯文哲"]):
        return True

    return False

# ======================
# 錯字修正（簡易）
# ======================
def fix_query(q: str) -> str:
    q = normalize(q)

    corrections = {
        "韓國玉": "韓國瑜",
        "柯p": "柯文哲",
        "蔡依林英文": "蔡英文"
    }

    for k, v in corrections.items():
        if k in q:
            q = q.replace(k, v)

    return q

# ======================
# AI 回答層
# ======================
def generate_answer(q, ptt, reddit):

    q = fix_query(q)
    base = ptt + reddit

    # 沒資料
    if not base:
        return "這種查詢目前沒人在乎，你查到這裡其實也不會多一個答案。"

    # 亂輸入
    if len(q.strip()) <= 1:
        return "你這輸入看起來像亂打的，先打清楚再來查。"

    # 一般模板
    general_templates = [
        "這題其實早就有人問過了。",
        "資料本來就混在一起，沒有標準答案。",
        "這種問題再查一次結果也不會變。",
        "各種來源說法不同，本來就沒有結論。",
        "這類問題就是資訊分歧。"
    ]

    # 政治模板
    politics_templates = [
        "政治問題本來就沒有共識。",
        "不同立場各說各話。",
        "這種議題本質就是對立，不會有答案。",
        "網路討論最後都會變成立場問題。",
        "政治議題沒有單一結論。"
    ]

    templates = politics_templates if is_politics(q) else general_templates

    return random.choice(templates)

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
