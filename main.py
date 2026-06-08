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
# AI 回答層
# ======================
def generate_answer(q, ptt, reddit):

    base = ptt + reddit

    # ======================
    # 沒資料
    # ======================
    if not base:
        return f"💬 系統回應：這種查詢目前沒人在乎，你查到這裡其實也不會多一個答案。"

    # ======================
    # 一般模板
    # ======================
    general_templates = [
        "→ {q} 這個其實早就有人問過了",
        "有人整理過但你應該沒爬文",
        "這問題是不是有點懶",
        "看起來就是標題農場集合",
        "基本上沒有統一答案啦",
        "這種東西每次都會戰起來"
    ]

    # ======================
    # 政治模板
    # ======================
    politics_templates = [
        "→ 政治文通常最後都會吵成一團，不意外",
        "八卦板看到這種問題就是準備開戰",
        "又是一個標準爭議議題",
        "這種東西通常沒有共識，只有立場",
        "討論前建議先確認資訊來源"
    ]

    # ======================
    # 選模板
    # ======================
    if is_politics(q):
        templates = politics_templates
    else:
        templates = general_templates

    roast = random.choice(templates).format(q=q)

    # ======================
    # 摘要
    # ======================
    keywords = []
    for x in base:
        keywords += x.replace("[", "").replace("]", "").split()[:2]

    keywords = list(set(keywords))[:6]
    summary = "、".join(keywords) if keywords else "資訊碎片化"

    # ======================
    # 整理結果
    # ======================
    ptt_lines = ptt[:3] if ptt else ["PTT無資料"]
    reddit_lines = reddit[:3] if reddit else ["Reddit無資料"]

    return f"""
🔥 系統分析
{roast}

🧠 網路摘要
{summary}

📌 討論狀態
PTT: {ptt_lines}
Reddit: {reddit_lines}

💬 結論
你自己判斷，不用再問一次。
""".strip()

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
