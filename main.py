
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
        " 有人整理過但你應該沒爬文",
        " 這問題是不是有點懶",
        " 看起來就是標題農場集合",
        " 基本上沒有統一答案啦",
        "這種東西每次都會戰起來"
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
    # 🔴 政治爭議模式（加強戰場感）
    # ======================
    politics_templates = [
        "→ 政治文通常最後都會吵成一團，不意外",
        "噓 八卦板看到這種問題就是準備開戰",
        "推 又是一個標準爭議議題",
        "→ 這種東西通常沒有共識，只有立場",
        "噓 討論前建議先確認資訊來源"
    ]
  politics_keywords = [
        "政府", "選舉", "總統", "立委", "政策",
        "台灣", "柯文哲", "賴清德", "侯友宜",
        "韓國瑜", "蔡英文", "陳水扁", "阿扁"
    ]

    is_politics = any(k in q for k in politics_keywords)

    if topic == "politics":
        opener = random.choice(politics_templates).format(q=q)
    else:
        opener = random.choice(general_templates).format(q=q)
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
