# src/relation.py
import re


def extract_dual_relations(text):
    """
    高级双路解构引擎（给离线清洗数据 build_graph_data.py 用的）
    """
    if not isinstance(text, str):
        return {"dynamic": [], "static": []}

    dynamic_edges = []
    static_edges = []

    pattern_dynamic = re.compile(r"撤销(?P<old_name>[^，。、；]+).*?设立(?P<new_name>[^，。、；]+)")
    pattern_static = re.compile(r"^(?P<parent>.*?[省市州盟自治区])(?P<child>.+?[市区县旗])$")

    match_dyn = pattern_dynamic.search(text)
    if match_dyn:
        old_name = match_dyn.group('old_name').strip()
        new_name = match_dyn.group('new_name').strip()

        dynamic_edges.append({
            "source_node": old_name, "relation": "变更设立", "target_node": new_name, "type": "dynamic"
        })

        match_sta = pattern_static.search(new_name)
        if match_sta:
            static_edges.append({
                "source_node": match_sta.group('child'), "relation": "隶属于", "target_node": match_sta.group('parent'),
                "type": "static"
            })

    return {"dynamic": dynamic_edges, "static": static_edges}


def extract_relations(text):
    """
    兼容接口（专门给 app.py 用的）
    确保返回的是一个【列表 List】，防止 extend() 函数把它拆碎！
    """
    dual_result = extract_dual_relations(text)
    # 将动态边和静态边合并成一个大的列表返回
    return dual_result["dynamic"] + dual_result["static"]
