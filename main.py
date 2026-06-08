from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# ======================
# Reddit（爬蟲版，不用 API）
# ======================
def get_reddit(q):
    url = f"https://www.reddit.com/search/?q={q}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for t in soup.find_all("h3"):
        results.append(t.text)

    return results[:5]


# ======================
# PTT
# ======================
def get_ptt(q):
    url = f"https://www.ptt.cc/bbs/Gossiping/search?q={q}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, cookies={"over18": "1"})
    soup = BeautifulSoup(res.text, "html.parser")

    return [t.text.strip() for t in soup.select(".title a")][:5]


# ======================
# API
# ======================
@app.get("/search")
def search(q: str):

    reddit_results = get_reddit(q)
    ptt_results = get_ptt(q)

    return {
        "query": q,
        "reddit": reddit_results,
        "ptt": ptt_resultsfrom fastapi.responses import FileResponse

@app.get("/")
def home():
    return FileResponse("static/index.html")
    }
