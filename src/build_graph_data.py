import pandas as pd
import os

# 导入你刚刚在 relation.py 里写好的高级引擎
from relation import extract_dual_relations

def main():
    # ================= 1. 智能定位路径 (告别绝对路径) =================
    # 自动定位项目根目录下的 data 文件夹
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_FILE = os.path.join(BASE_DIR, "data", "mca_dynamic_changes.csv")
    STATIC_OUTPUT = os.path.join(BASE_DIR, "data", "static_edges.csv")
    DYNAMIC_OUTPUT = os.path.join(BASE_DIR, "data", "dynamic_edges.csv")

    print(f"🚀 开始加载语料：{INPUT_FILE}")
    if not os.path.exists(INPUT_FILE):
        print("❌ 错误：找不到原始数据文件！请检查 spider.py 是否成功运行。")
        return

    df = pd.read_csv(INPUT_FILE)

    static_triplets = []
    dynamic_triplets = []

    # ================= 2. 启动双路数据解构 =================
    print("正在进行双路数据解构...")
    for index, row in df.iterrows():
        text = row['raw_text']
        # 调用 relation.py 里的函数
        result = extract_dual_relations(text)

        # 将结果分别塞进两个列表
        dynamic_triplets.extend(result["dynamic"])
        static_triplets.extend(result["static"])

    # 转换为 DataFrame 并去重
    df_static = pd.DataFrame(static_triplets).drop_duplicates()
    df_dynamic = pd.DataFrame(dynamic_triplets).drop_duplicates()

    print(f"✅ 解构完毕！")
    print(f"📊 提取到静态隶属边（纵向层级树）：{len(df_static)} 条")
    print(f"📊 提取到动态变更边（横向历史演变）：{len(df_dynamic)} 条")

    # ================= 3. 保存最终边表 =================
    # 确保存储目录存在
    os.makedirs(os.path.dirname(STATIC_OUTPUT), exist_ok=True)

    df_static.to_csv(STATIC_OUTPUT, index=False, encoding="utf-8-sig")
    df_dynamic.to_csv(DYNAMIC_OUTPUT, index=False, encoding="utf-8-sig")

    print(f"\n💾 两张核心图谱边表已安全导出至 data/ 目录！")
    print("👉 数据处理流程彻底打通，可以让前端同学开始画图啦！")

if __name__ == "__main__":
    main()