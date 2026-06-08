from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
from bs4 import BeautifulSoup
import random
import re

app = FastAPI()

# ======================
# Reddit（內部資料源）
# ======================
def get_reddit(q):
    url = f"https://www.reddit.com/search.json?q={q}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()
        return [c["data"]["title"] for c in data["data"]["children"]][:5]
    except:
        return []

# ======================
# PTT（內部資料源）
# ======================
def get_ptt(q):
    url = f"https://www.ptt.cc/bbs/Gossiping/search?q={q}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(
            url,
            headers=headers,
            cookies={"over18": "1"},
            timeout=5
        )
        soup = BeautifulSoup(res.text, "html.parser")
        return [t.text.strip() for t in soup.select(".title a")][:5]
    except:
        return []

# ======================
# 政治判斷
# ======================
def is_politics(q: str) -> bool:
    qn = re.sub(r"\s+", "", q)

    keywords = [
        "政府", "選舉", "總統", "立委", "政策",
        "台灣", "政治", "政黨", "內閣", "立法院", "行政院",
        "民進黨", "國民黨", "民眾黨",
        "柯文哲", "賴清德", "侯友宜", "韓國瑜",
        "蔡英文", "陳水扁", "阿扁",
        "柯p", "小英", "賴神", "韓導", "阿北"
    ]

    return any(k in qn for k in keywords)

# ======================
# 亂輸入判斷（注音 / 鍵盤亂打）
# ======================
def is_messy_input(q: str) -> bool:
    q = q.strip()

    if len(q) <= 1:
        return True

    if re.fullmatch(r"[^\u4e00-\u9fffA-Za-z0-9]+", q):
        return True

    if len(set(q)) <= 2 and len(q) > 3:
        return True

    gibberish = ["asdf", "qwe", "zxc", "jkl", "ㄅㄆㄇ"]
    if any(g in q.lower() for g in gibberish):
        return True

    return False


# ======================
# 🔥 核心 AI 搜尋引擎
# ======================
def generate_answer(q, ptt, reddit):

    base = ptt + reddit

    # ======================
    # 1️⃣ 亂輸入（優先嗆）
    # ======================
    if is_messy_input(q):
        return "你這輸入是認真的嗎？先把字打好再來查。"

    # ======================
    # 2️⃣ 沒資料
    # ======================
    if not base:
        return "這題幾乎沒人在討論，你查到這裡也不會多一個答案。"

    # ======================
    # 3️⃣ 合併語意（但不顯示來源）
    # ======================
    merged_text = " ".join(base)

    keywords = list(set(
        word for word in re.split(r"\W+", merged_text) if len(word) > 1
    ))[:6]

    keyword_str = "、".join(keywords) if keywords else "資訊分散"

    # ======================
    # 4️⃣ 主結論模板（嗆但合理）
    # ======================
    if is_politics(q):
        templates = [
            "這題本質就是立場問題，不是資訊問題，問再多也不會有共識。",
            "政治議題永遠都在各說各話，不存在客觀答案。",
            "這種東西本來就會被不同立場重新解釋，沒有標準解。",
            "看起來像在問問題，其實是在選立場。",
            "結論很簡單：這題沒有結論。"
        ]
    else:
        templates = [
            "這題沒有單一答案，各種說法本來就會互相矛盾。",
            "資訊來源本來就分散，你看到的只是不同版本。",
            "這問題本身就沒有固定解，只是大家講法不同。",
            "整理完的結果就是：沒有一致結論。",
            "你再查一次，也不會得到不一樣答案。"
        ]

    base_answer = random.choice(templates)

    # ======================
    #  額外嗆人補強
    # ======================
    roast_addons = [
        "這種問題其實不用想太複雜。",
        "很多人問過，但答案一直都一樣。",
        "你覺得混亂只是因為本來就沒答案。",
        "這題再查十次結果也不會變。"
    ]

    roast = random.choice(roast_addons)

    # ======================
    #  最終輸出（乾淨搜尋引擎）
    # ======================
    return f"""
🧠 搜尋結論
{base_answer}

📌 特徵關鍵詞
{keyword_str}

💬 補充判斷
{roast}
""".strip()


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

    return {
        "answer": generate_answer(q, ptt, reddit)
    }
