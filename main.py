from fastapi import FastAPI
import praw
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# ======================
# Reddit 設定
# ======================
reddit = praw.Reddit(
    client_id="你的client_id",
    client_secret="你的client_secret",
    user_agent="gxxgle-it"
)

# ======================
# PTT crawler
# ======================
def get_ptt(keyword):
    url = f"https://www.ptt.cc/bbs/Gossiping/search?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, cookies={"over18": "1"})
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for t in soup.select(".title a"):
        results.append(t.text.strip())

    return results


# ======================
# API
# ======================
@app.get("/search")
def search(q: str):

    # Reddit
    reddit_results = []
    try:
        for post in reddit.subreddit("all").search(q, limit=5):
            reddit_results.append(post.title)
    except:
        reddit_results = ["Reddit error"]

    # PTT
    try:
        ptt_results = get_ptt(q)
    except:
        ptt_results = ["PTT error"]

    # 合併（藝術化輸出）
    return {
        "query": q,
        "reddit": reddit_results,
        "ptt": ptt_results
    }
