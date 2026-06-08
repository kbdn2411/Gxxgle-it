import re
import random

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
# 亂輸入判斷（你缺這個）
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
# AI 回答
# ======================
def generate_answer(q, ptt, reddit):

    base = ptt + reddit

    # ======================
    # 錯字 / 亂輸入（優先）
    # ======================
    if is_messy_input(q):
        return "你這輸入看起來像亂打的，先打清楚再來查。"

    # ======================
    # 沒資料
    # ======================
    if not base:
        return "這種查詢目前沒人在乎，你查到這裡其實也不會多一個答案。"

   # ======================
# 一般模板（加強嗆感）
# ======================
general_templates = [
    "這題其實早就有人問過了，你只是懶得查。",
    "資料本來就亂成一團，你還想要標準答案？",
    "這種問題再查十次結果也一樣，不會變。",
    "各種來源互打，你以為會有結論？想太多。",
    "這類問題本來就沒有答案，還一直問有點多餘。"
]

# ======================
# 政治模板（加強戰場感）
# ======================
politics_templates = [
    "政治問題本來就不可能有共識，問再多也一樣吵。",
    "這種議題講白了就是立場問題，不是知識問題。",
    "網路上早就各說各話，你再查也是一樣混亂。",
    "這種東西本來就沒有正解，只是看你站哪邊。",
    "政治討論最後都會變成互相說服失敗的場面。"
]
    ]

    # ======================
    # 判斷模式
    # ======================
    templates = politics_templates if is_politics(q) else general_templates

    return random.choice(templates)
