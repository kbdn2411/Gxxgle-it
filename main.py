from fastapi import FastAPI
import praw

app = FastAPI()

reddit = praw.Reddit(
    client_id="你的client_id",
    client_secret="你的client_secret",
    user_agent="gxxgle-it"
)

@app.get("/search")
def search(q: str):
    results = []

    for post in reddit.subreddit("all").search(q, limit=5):
        results.append(post.title)

    return {"results": results}
