# src/build_graph_data.py
import pandas as pd
import os
from relation import extract_dual_relations


def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_FILE = os.path.join(BASE_DIR, "data", "mca_dynamic_changes.csv")
    STATIC_OUTPUT = os.path.join(BASE_DIR, "data", "static_edges.csv")
    DYNAMIC_OUTPUT = os.path.join(BASE_DIR, "data", "dynamic_edges.csv")

    print(f"🚀 开始加载语料：{INPUT_FILE}")
    if not os.path.exists(INPUT_FILE):
        print("❌ 错误：找不到原始数据文件！")
        return

    df = pd.read_csv(INPUT_FILE)
    static_triplets, dynamic_triplets = [], []

    print("正在进行双路数据解构...")
    for index, row in df.iterrows():
        result = extract_dual_relations(row['raw_text'])
        dynamic_triplets.extend(result["dynamic"])
        static_triplets.extend(result["static"])

    df_static = pd.DataFrame(static_triplets).drop_duplicates()
    df_dynamic = pd.DataFrame(dynamic_triplets).drop_duplicates()

    os.makedirs(os.path.dirname(STATIC_OUTPUT), exist_ok=True)
    df_static.to_csv(STATIC_OUTPUT, index=False, encoding="utf-8-sig")
    df_dynamic.to_csv(DYNAMIC_OUTPUT, index=False, encoding="utf-8-sig")

    print(f"✅ 解构完毕！成功提取 静态隶属边 {len(df_static)} 条，动态演化边 {len(df_dynamic)} 条。")
    print(f"💾 两张核心图谱边表已安全导出至 data/ 目录！")


if __name__ == "__main__":
    main()