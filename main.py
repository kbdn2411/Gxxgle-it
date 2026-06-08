import re
import random

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
# 政治判斷（完整語意版）
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

        "新聞", "訪美", "外交", "川普", "拜登",
        "中國", "美國", "兩岸"
    ]

    return any(k in qn for k in keywords)


# ======================
# 語意壓縮（PTT + Reddit融合）
# ======================
def merge_results(results: list) -> str:
    text = " ".join(results)
    words = re.split(r"[^\w\u4e00-\u9fff]+", text)

    cleaned = list(set(w for w in words if len(w) > 1))
    return "、".join(cleaned[:6]) if cleaned else "資訊破碎"


# ======================
# AI 核心輸出
# ======================
def generate_answer(q: str, base: list):

    # 1️⃣ 亂輸入
    if is_messy_input(q):
        return "你這輸入是認真的嗎？先把字打好再來查。"

    # 2️⃣ 沒資料
    if not base:
        return "這題本身就沒什麼人在討論，查再多也不會變出答案。"

    # 3️⃣ 語意整合（不顯示來源）
    summary = merge_results(base)

    # 4️⃣ 分流模板（嗆但穩）
    if is_politics(q):
        templates = [
            "這題不是資訊問題，是立場問題，本來就沒有客觀答案。",
            "不同陣營各講各話，你看到的只是包裝過的版本。",
            "這種議題本來就注定沒有共識。",
            "表面在討論，其實只是立場對撞。",
            "結論很簡單：這題不存在解答。"
        ]
    else:
        templates = [
            "這題沒有唯一答案，本來就是資訊分裂。",
            "你看到的是不同版本，不是錯誤。",
            "再查一次結果也不會改變。",
            "資訊來源本來就混亂。",
            "本質就是沒有統一結論。"
        ]

    # 5️⃣ 嗆補刀（強化版但不亂）
    addons = [
        "不用再查了，答案不會變。",
        "你覺得亂只是因為本來就沒有答案。",
        "再看也只是同樣結果。",
        "這題根本不值得繼續追。",
        "你在找的是不存在的確定性。"
    ]

    main = random.choice(templates)
    extra = random.choice(addons)

    # 6️⃣ 乾淨輸出（無PTT/Reddit/AI字樣）
    return f"{main}（{summary}） {extra}"


# ======================
# 模擬搜尋入口（之後可接 API）
# ======================
def search_engine(q: str):

    # 模擬 PTT + Reddit 已整合結果
    ptt_results = [f"{q} 討論：立場不同", f"{q} 爭議：無定論"]
    reddit_results = [f"{q} opinion mixed", f"{q} debate ongoing"]

    base = ptt_results + reddit_results

    return {
        "answer": generate_answer(q, base)
    }


# ======================
# CLI 測試
# ======================
if __name__ == "__main__":
    while True:
        q = input("Search: ")
        print(search_engine(q)["answer"])
