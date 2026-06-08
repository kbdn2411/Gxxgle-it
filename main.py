from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允許前端連線（很重要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👉 你的「Reddit / PTT 資料庫」（先用假資料）
texts = [
    "Google怎麼用？先打開搜尋引擎",
    "你現在就在用還問",
    "笑死這也要問",
    "PTT用瀏覽器啊",
    "不會google嗎",
    "先查再問",
    "這種問題也敢發"
]

# 👉 搜尋API
@app.get("/search")
def search(q: str):
    q = q.lower()

    results = []

    for t in texts:
        # 超簡單匹配（先不要AI）
        if any(word in t.lower() for word in q.split()):
            results.append(t)

    # 如果沒匹配到，給預設酸民回覆
    if not results:
        results = [
            "這也要問？",
            "先Google很難嗎？",
            "自己查一下不會？"
        ]

    return {"results": results}
