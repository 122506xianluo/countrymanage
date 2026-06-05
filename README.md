
# 行政区划历史变更分析系统（适配 raw_text 数据）

## 当前 CSV 格式

系统已经适配：

source,raw_text

其中：

- source：数据来源
- raw_text：原始行政区划变更文本

## 运行方法

1. 安装依赖

pip install -r requirements.txt

2. 运行项目

python app.py

3. 打开浏览器

http://127.0.0.1:5000

## 项目功能

- NER 命名实体识别
- RE 关系抽取
- 分类任务
- 知识图谱
- 时序统计
- Flask 可视化页面
