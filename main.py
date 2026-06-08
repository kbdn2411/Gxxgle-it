from fastapi import FastAPI
from fastapi.responses import FileResponse
import random
import os

app = FastAPI()

# ======================
# AI 回答池（隨機但穩定）
# ======================
answers = [
    "這題本質就是資訊分裂，沒有唯一答案。",
    "你看到的是不同版本，不是錯誤。",
    "這種問題再查一次結果也不會變。",
    "資訊來源本來就混亂，不可能統一。",
    "結論很簡單：沒有結論。",
    "你以為在找答案，其實是在找立場。"
]

# ======================
# API
# ======================
@app.get("/search")
def search(q: str = ""):
    return {
        "query": q,
        "answer": random.choice(answers)
    }

# ======================
# UI
# ======================
@app.get("/")
def home():
    return FileResponse("static/index.html")
