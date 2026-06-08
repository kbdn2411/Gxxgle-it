
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

    all_text = " ".join(ptt + reddit)

    if not all_text:
        return f"關於「{q}」目前網路討論資料不足，無法形成明確共識。"

    return f"""
關於「{q}」的網路討論整理如下：

🔹 PTT 與 Reddit 的主要內容顯示：
{ptt[0] if ptt else "PTT無資料"}

🔹 社群討論方向：
{reddit[0] if reddit else "Reddit無資料"}

📌 總結：
此議題在網路上的討論多為意見與新聞標題延伸，並沒有單一標準答案，但可以看出社群主要關注標題所反映的事件與爭議。
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
