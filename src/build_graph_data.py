import os
import pandas as pd


def merge_static_and_dynamic_data():
    # ---- 1. 设定路径 ----
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )  # 定位到项目根目录
    DIVID_FILE = os.path.join(BASE_DIR, "data", "divisions.csv")
    DYN_EDGE_FILE = os.path.join(BASE_DIR, "data", "dynamic_edges.csv")

    OUTPUT_TOTAL_EDGES = os.path.join(BASE_DIR, "data", "total_graph_edges.csv")

    print("🚀 开始进行全量数据融合流水线...")

    # ---- 2. 加载数据 ----
    if not os.path.exists(DIVID_FILE) or not os.path.exists(DYN_EDGE_FILE):
        print("❌ 错误：缺少必要的输入源文件，请检查 data 文件夹！")
        return

    df_div = pd.read_csv(DIVID_FILE)  # 60万静态基础数据
    df_dyn = pd.read_csv(DYN_EDGE_FILE)  # 爬虫抽取的动态演变数据

    # ---- 3. 第一步：将静态区划表转化为关系三元组 ----
    print("⏳ 正在将 60 万静态区划解构为层级隶属树...")

    # 建立 code -> name 的高精度快速索引字典
    code_to_name = dict(zip(df_div["code"], df_div["name"]))

    # 通过 parent_code 映射出父级节点的名称
    df_div["parent_name"] = df_div["parent_code"].map(code_to_name)

    # 过滤掉没有父节点的最顶层（如国家级或无上级节点数据）
    df_static_edges = df_div[df_div["parent_name"].notna()].copy()

    # 重命名列名，对齐知识图谱的标准三元组表头
    df_static_tree = pd.DataFrame(
        {
            "source_node": df_static_edges["name"],
            "relation": "隶属于",
            "target_node": df_static_edges["parent_name"],
            "type": "STATIC",
        }
    )

    print(f"✅ 静态层级树转换成功，生成静态边：{len(df_static_tree)} 条。")

    # ---- 4. 第二步：将静态边与动态边做矩阵矩阵拼接 ----
    print("⏳ 正在进行动静态边数据全量归并...")

    # 规范动态变更数据的类型标签
    df_dyn["type"] = "DYNAMIC"

    # 强力拼接两个 DataFrame
    df_total_edges = pd.concat([df_static_tree, df_dyn], ignore_index=True)

    # ---- 5. 第三步：去重与容错治理 ----
    initial_count = len(df_total_edges)
    df_total_edges.drop_duplicates(
        subset=["source_node", "relation", "target_node"], inplace=True
    )
    final_count = len(df_total_edges)
    print(f"✂️ 数据去重完毕，过滤掉重复边：{initial_count - final_count} 条。")

    # ---- 6. 结果持久化入库 ----
    df_total_edges.to_csv(OUTPUT_TOTAL_EDGES, index=False, encoding="utf-8")
    print(
        f"🎯 全量动静态图谱基座合并完成！最终边总数：{final_count} 条。已保存至：{OUTPUT_TOTAL_EDGES}"
    )


if __name__ == "__main__":
    merge_static_and_dynamic_data()