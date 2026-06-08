
from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# ======================
# Reddit（JSON穩定版）
# ======================
def get_reddit(q):
    url = f"https://www.reddit.com/search.json?q={q}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()

        return [
            child["data"]["title"]
            for child in data["data"]["children"]
        ][:5]
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
# AI 回答層（重點）
# ======================
import random

def generate_answer(q, ptt, reddit):

    if not ptt and not reddit:
        return f"→ {q} 這種問題現在沒人討論\n噓 這種東西也要問?"

    base = ptt + reddit

    templates = [
        "→ {q} 這個其實早就有人問過了",
        "推 有人整理過但你應該沒爬文",
        "噓 這問題是不是有點懶",
        "→ 看起來就是標題農場集合",
        "推 基本上沒有統一答案啦",
        "→ 這種東西每次都會戰起來"
    ]

    roast = random.choice(templates).format(q=q)
    # ===== 3. 最終輸出 =====
    return f"""
🧠 網路摘要：
從 PTT / Reddit 觀察，主要關鍵詞是：{summary}

📌 討論狀態：
{ptt[:3] if ptt else "PTT無資料"}
{reddit[:3] if reddit else "Reddit無資料"}

😏 AI吐槽：
{roast}

💬 結論：
網路上的資訊不是沒有，而是每個人都講得不一樣，所以看起來就像沒有答案。
"""

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

    answer = generate_answer(q, ptt, reddit)

    return {
        "query": q,
        "answer": answer,
        "ptt": ptt,
        "reddit": reddit
    }
