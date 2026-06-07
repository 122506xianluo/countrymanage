# src/ner.py
import re


def extract_entities(text):
    """
    实体抽取模块：专门提取文本中的行政区划地名，供前端渲染展示。
    """
    if not isinstance(text, str):
        return []

    # 提取所有带有行政级别后缀的中文词汇
    entities = re.findall(r"[\u4e00-\u9fa5]+?[省市州盟区县乡镇街道]", text)

    # 去重后返回列表
    return list(set(entities))