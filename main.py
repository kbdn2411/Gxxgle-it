
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
def generate_answer(q, ptt, reddit):

    combined = ptt + reddit

    if not combined:
        return f"你問「{q}」但網路上連吵都沒人吵，這問題的存在感比 WiFi 訊號還弱。"

    # ===== 1. 摘要（抓關鍵字）=====
    keywords = []

    for text in combined[:10]:
        words = text.replace("[", "").replace("]", "").split()
        keywords.extend(words[:3])  # 簡單粗暴抽詞

    keywords = list(set(keywords))[:5]

    summary = "、".join(keywords) if keywords else "無明確關鍵詞"

    # ===== 2. 酸回邏輯 =====
    if "嗎" in q or "?" in q:
        roast = "這問題你自己查一下其實比較快，不過既然你問了，答案大概是大家也沒共識。"
    elif "有沒有" in q:
        roast = "有，但討論內容跟你期待的答案通常不太一樣。"
    else:
        roast = "這種問題在網路上通常只會越查越混亂，不會越查越清楚。"

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
