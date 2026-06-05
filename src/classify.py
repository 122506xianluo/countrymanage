
def classify_text(text):

    if "设立" in text:
        return "新设"

    if "撤销" in text:
        return "撤销"

    if "更名" in text:
        return "更名"

    if "合并" in text:
        return "合并"

    if "拆分" in text:
        return "拆分"

    return "其他"
