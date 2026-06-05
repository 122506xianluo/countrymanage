
import re

def extract_relations(text):

    relations = []

    belong_matches = re.findall(
        r"([\\u4e00-\\u9fa5]{2,10}(?:县|市|区))由([\\u4e00-\\u9fa5]{2,20})管辖",
        text
    )

    for source, target in belong_matches:
        relations.append((
            source,
            "由...管辖",
            target
        ))

    setup_matches = re.findall(
        r"设立([\\u4e00-\\u9fa5]{2,10}(?:县|市|区))",
        text
    )

    for area in setup_matches:
        relations.append((
            area,
            "类型",
            "新设行政区"
        ))

    return relations
