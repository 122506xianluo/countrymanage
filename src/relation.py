import re


def extract_relations(text):
    """
    高级双路解构引擎：同时提取时间维度（动态变更边）和空间维度（静态隶属边）
    """
    if not isinstance(text, str):
        return {"dynamic": [], "static": []}

    dynamic_edges = []
    static_edges = []

    # 核心正则：标点符号边界提取与层级劈裂
    pattern_dynamic = re.compile(r"撤销(?P<old_name>[^，。、；]+).*?设立(?P<new_name>[^，。、；]+)")
    pattern_static = re.compile(r"^(?P<parent>.*?[省市州盟自治区])(?P<child>.+?[市区县旗])$")

    match_dyn = pattern_dynamic.search(text)
    if match_dyn:
        old_name = match_dyn.group('old_name').strip()
        new_name = match_dyn.group('new_name').strip()

        # 1. 记录动态边（前世今生）
        dynamic_edges.append({
            "source_node": old_name,
            "relation": "变更设立",
            "target_node": new_name,
            "type": "dynamic"
        })

        # 2. 记录静态边（对新名字进行二次解构，寻找上级）
        match_sta = pattern_static.search(new_name)
        if match_sta:
            static_edges.append({
                "source_node": match_sta.group('child'),
                "relation": "隶属于",
                "target_node": match_sta.group('parent'),
                "type": "static"
            })

    return {"dynamic": dynamic_edges, "static": static_edges}
