import random
import re

# ======================
# 亂輸入判斷
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
# 政治判斷
# ======================
def is_politics(q: str) -> bool:

    qn = re.sub(r"\s+", "", q)

    keywords = [
        "政府", "選舉", "總統", "立委", "市長", "縣長",
        "政策", "政治", "政黨", "內閣",
        "立法院", "行政院",

        "民進黨", "國民黨", "民眾黨",

        "柯文哲", "賴清德", "侯友宜", "韓國瑜",
        "蔡英文", "陳水扁", "馬英九",

        "柯p", "阿北", "小英", "賴神", "韓導",

        "新聞", "訪美", "外交", "川普", "拜登", "中國", "美國"
    ]

    return any(k in qn for k in keywords)


# ======================
# AI 回答核心
# ======================
def generate_answer(q, ptt=None, reddit=None):

    # 避免 None crash
    ptt = ptt or []
    reddit = reddit or []

    base = ptt + reddit

    # 1️⃣ 亂輸入
    if is_messy_input(q):
        return "你這輸入是認真的嗎？先把字打好再來查。"

    # 2️⃣ 沒資料
    if not base:
        return "這題沒什麼人在討論，查再多也不會變出答案。"

    # 3️⃣ 模板
    if is_politics(q):
        templates = [
            "這題就是立場問題，沒有共識可言。",
            "政治議題本來就只會變成互相對立。",
            "不同陣營講法完全不一樣，沒有標準答案。",
            "你看到的不是資訊，是立場包裝。",
            "這題本質就是對立，不是解答。"
        ]
    else:
        templates = [
            "這題沒有唯一答案，本來就會互相矛盾。",
            "資訊來源不同，所以看起來才會混亂。",
            "這種問題再查一次結果也不會改變。",
            "你看到的是不同版本，不是錯誤。",
            "本質就是資訊分散，沒有統一解。"
        ]

    main = random.choice(templates)

    addons = [
        "不用再查了，結果不會變。",
        "你會覺得亂只是因為本來就沒答案。",
        "再看一次也不會更清楚。",
        "這題本來就沒有標準解。",
        "結論很明顯，但你一直在找不存在的答案。"
    ]

    extra = random.choice(addons)

    return f"{main} {extra}"
