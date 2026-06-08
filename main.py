
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import praw
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# 允許前端呼叫（很重要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reddit（記得填 API）
reddit = praw.Reddit(
    client_id="你的client_id",
    client_secret="你的client_secret",
    user_agent="gxxgle-it"
)

# PTT crawler
def get_ptt(q):
    url = f"https://www.ptt.cc/bbs/Gossiping/search?q={q}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, cookies={"over18": "1"})
    soup = BeautifulSoup(res.text, "html.parser")

    return [t.text.strip() for t in soup.select(".title a")]

@app.get("/search")
def search(q: str):

    reddit_results = []
    try:
        for post in reddit.subreddit("all").search(q, limit=5):
            reddit_results.append(post.title)
    except:
        reddit_results = ["Reddit error"]

    try:
        ptt_results = get_ptt(q)
    except:
        ptt_results = ["PTT error"]

    return {
        "query": q,
        "reddit": reddit_results,
        "ptt": ptt_results
    }
