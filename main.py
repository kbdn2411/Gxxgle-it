from fastapi import FastAPI
import re
import random

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
# 政治判斷
# ======================
def is_politics(q: str) -> bool:
    qn = re.sub(r"\s+", "", q)

    keywords = [
        "政府","選舉","總統","立委","市長","縣長",
        "政治","政黨","內閣","立法院","行政院",
        "民進黨","國民黨","民眾黨",
        "柯文哲","賴清德","侯友宜","韓國瑜",
        "蔡英文","陳水扁","馬英九",
        "柯p","阿北","小英","賴神","韓導",
        "新聞","外交","訪問","中國","美國","川普","拜登"
    ]

    return any(k in qn for k in keywords)


# ======================
# 核心回答（嗆版）
# ======================
def generate_answer(q: str) -> str:

    # 1️⃣ 亂輸入
    if is_messy_input(q):
        return "你這輸入是來亂的？先把字打正常再來問。"

    # 2️⃣ 政治模式（更嗆）
    if is_politics(q):
        templates = [
            "這種政治問題講再多也沒用，本來就是立場互打。",
            "不用期待有答案，這題就是陣營對撞現場。",
            "你看到的不是資訊，是不同派系的包裝版本。",
            "政治問題問結論？這本身就很天真。",
            "這題的唯一共識就是沒有共識。"
        ]
        addons = [
            "不用再腦補答案了。",
            "查再多也只是換個立場看法。",
            "你只是把自己丟進輿論戰場。",
        ]

    # 3️⃣ 一般模式（也嗆）
    else:
        templates = [
            "這題沒有標準答案，你再查也不會變聰明。",
            "資訊本來就亂，你只是剛好撞到混亂現場。",
            "這種問題本質就是沒有解，別硬找。",
            "不同來源互打，你還想整理成結論？",
            "你看到的不是答案，是一堆版本。"
        ]
        addons = [
            "不用再查第二次，結果一樣。",
            "這題本來就不會讓你滿意。",
            "你只是想要不存在的確定答案。",
        ]

    main = random.choice(templates)
    extra = random.choice(addons)

    return f"{main} {extra}"


# ======================
# API
# ======================
@app.get("/search")
def search(q: str):
    return {
        "result": generate_answer(q)
    }
