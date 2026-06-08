from fastapi import FastAPI
import random
import re

app = FastAPI()

# ======================
# 亂輸入判斷
# ======================
def is_messy_input(q: str) -> bool:
    q = q.strip()

    if len(q) <= 1:
        return True

    if re.fullmatch(r"[^\u4e00-\u9fffA-Za-z0-9]+", q):
        return True

    gibberish = ["asdf", "qwe", "zxc", "jkl", "ㄅㄆㄇ"]
    if any(g in q.lower() for g in gibberish):
        return True

    if len(set(q)) <= 2 and len(q) > 3:
        return True

    return False


# ======================
# 政治判斷（穩定版）
# ======================
def is_politics(q: str) -> bool:
    qn = re.sub(r"\s+", "", q)

    keywords = [
        "政府","選舉","總統","立委","市長","縣長",
        "政策","政治","政黨","內閣","立法院","行政院",
        "民進黨","國民黨","民眾黨",
        "柯文哲","賴清德","侯友宜","韓國瑜",
        "蔡英文","陳水扁","馬英九",
        "柯p","阿北","小英","賴神","韓導",
        "新聞","外交","訪美","川普","拜登","中國","美國"
    ]

    return any(k in qn for k in keywords)


# ======================
# 核心 AI（純一句話搜尋引擎）
# ======================
def generate_answer(q: str) -> str:

    # 1️⃣ 亂輸入
    if is_messy_input(q):
        return "你這輸入是認真的嗎？先把字打好再來查。"

    # 2️⃣ 政治模式
    if is_politics(q):
        templates = [
            "這題就是立場問題，沒有客觀答案。",
            "政治議題本來就只會變成立場對撞。",
            "不同陣營各說各話，不存在統一結論。",
            "你看到的是立場，不是事實本身。",
            "這題本質就是對立，不是解答。"
        ]
    else:
        templates = [
            "這題沒有唯一答案，本來就存在不同說法。",
            "資訊來源不同，所以結果自然會混亂。",
            "這種問題再查一次也不會改變結論。",
            "你看到的是不同版本，不是錯誤。",
            "本質就是資訊分散，沒有統一解。"
        ]

    main = random.choice(templates)

    # 3️⃣ 加強語氣（但不爆炸）
    addons = [
        "不用再查了，結果不會變。",
        "你會覺得亂只是因為本來就沒標準答案。",
        "再看一次也不會更清楚。",
        "這題本來就沒有唯一解。",
        "結論其實很固定，只是你不接受。"
    ]

    extra = random.choice(addons)

    return f"{main} {extra}"


# ======================
# API（極簡乾淨輸出）
# ======================
@app.get("/search")
def search(q: str):
    return {
        "answer": generate_answer(q)
    }
