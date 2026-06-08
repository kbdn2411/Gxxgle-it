from fastapi import FastAPI
import random

app = FastAPI()

# ======================
# 🔥 回答資料庫（你可以一直擴充）
# ======================

copypasta_pool = [
    "我已經看過太多次這種問題了，答案永遠一樣，但人類還是會問。",
    "你以為你在問問題，其實你只是重複歷史。",
    "這世界沒有標準答案，只有重複的錯誤。",
    "我不是不想回答，我是已經回答過太多次。",
    "當你開始問這個問題的時候，答案就已經不重要了。"
]

joke_pool = [
    "為什麼電腦很冷？因為它有很多風扇。",
    "我昨天問AI人生意義，它當機了。",
    "為什麼搜尋引擎很忙？因為大家都在問同一個問題。",
    "我不是懶，我只是進入省電模式。",
    "如果人生可以重來，我還是會點同樣的外送。"
]

serious_pool = [
    "根據資料分析，這類問題沒有單一解。",
    "系統顯示結果分歧，因此無法給出唯一答案。",
    "從統計上來看，不同來源會有不同結論。",
    "目前資訊不足以支持明確判斷。",
    "綜合判斷：結果依情境而異。"
]

chaos_pool = [
    "⚠ 系統錯誤：但我選擇繼續回答。",
    "這題我知道，但我不想讓你知道。",
    "答案存在，但被我隱藏了。",
    "你問的問題已被重新定義。",
    "資料正在逃跑中，請稍後再試。"
]

# ======================
# 🔥 隨機核心
# ======================
def random_engine(q: str):

    mode = random.choice(["copy", "joke", "serious", "chaos"])

    if mode == "copy":
        answer = random.choice(copypasta_pool)

    elif mode == "joke":
        answer = random.choice(joke_pool)

    elif mode == "serious":
        answer = random.choice(serious_pool)

    else:
        answer = random.choice(chaos_pool)

    return {
        "input": q,
        "mode": mode,
        "answer": answer
    }


# ======================
# API
# ======================
@app.get("/search")
def search(q: str):
    return random_engine(q)
