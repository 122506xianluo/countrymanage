# src/graph.py
import networkx as nx
from pyvis.network import Network
import os


def build_graph(relations):
    """
    基于关系字典列表，构建网络图并保存为可交互的 HTML 文件
    """
    G = nx.DiGraph()

    # ================= 1. 核心修复：安全的数据解包 =================
    for item in relations:
        # 手动通过字典的键把对应的值取出来，防止报错
        source = item.get("source_node")
        relation = item.get("relation")
        target = item.get("target_node")

        # 加上一个安全判断：如果成功取到了源节点和目标节点，才画到图谱上
        if source and target:
            G.add_node(source)
            G.add_node(target)
            G.add_edge(
                source,
                target,
                title=relation  # 鼠标悬停在连线上时会显示“变更设立”等文字
            )

    # ================= 2. 配置并生成前端图谱 =================
    net = Network(
        height="750px",
        width="100%",
        directed=True,  # 开启箭头指向
        neighborhood_highlight=True  # 开启高亮：点击一个节点，相关的节点会亮起
    )

    net.from_nx(G)

    # ================= 3. 智能路径修复 =================
    # 自动定位到项目根目录下的 templates 文件夹，无论在哪运行都不会找不到路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(BASE_DIR, "templates", "graph.html")

    # 确保 templates 文件夹存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 导出 HTML
    net.save_graph(output_path)

    return G