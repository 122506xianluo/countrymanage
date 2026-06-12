import re


def extract_dual_relations(text):
    """
    升级版抽取引擎：专职处理动态变更事件
    (静态隶属关系已交由官方 divisions.csv 处理，此处不再用正则猜测)
    """
    # 容错处理：如果传进来的不是纯文本，直接返回空字典
    if not isinstance(text, str):
        return {"dynamic": [], "static": []}

    dynamic_edges = []

    # 1. 专注动态变更提取（保留你原本的撤销/设立逻辑）
    pattern_dynamic = re.compile(r"撤销(?P<old_name>[^、，。]+).*?设立(?P<new_name>[^、，。]+)")

    match_dyn = pattern_dynamic.search(text)
    if match_dyn:
        old_name = match_dyn.group('old_name').strip()
        new_name = match_dyn.group('new_name').strip()

        dynamic_edges.append({
            "source_node": old_name,
            "relation": "变更设立",
            "target_node": new_name,
            "type": "DYNAMIC"  # 规范化分类标签
        })

    # 你可以在这里继续追加其他动态正则，比如“更名”的正则
    # pattern_rename = re.compile(r"(?P<old_name>.*?)更名为(?P<new_name>.*)")
    # ...

    # 2. 核心改动：不再生成 static_edges
    # 返回空的 static 列表，确保外部拆包逻辑 (result["static"]) 不会报错
    return {
        "dynamic": dynamic_edges,
        "static": []
    }
