import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
from urllib.parse import urljoin

# ================= 爬虫配置 =================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}


def get_article_links(index_url):
    """
    【阶段一】解析目录页，获取所有年份的文章链接
    """
    print(f"🔍 正在解析目录页: {index_url}")
    try:
        response = requests.get(index_url, headers=HEADERS, timeout=15)
        # 【核心修复】：放弃强转 UTF-8，让库自动推测网页的真实编码（解决 GBK 乱码问题）
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'html.parser')

        # 锁定存放链接的专属 div 容器
        tz_con = soup.find('div', class_='tz_con')

        links = []
        if tz_con:
            for a_tag in tz_con.find_all('a'):
                href = a_tag.get('href')
                if href:
                    full_url = urljoin(index_url, href)  # 拼接绝对路径
                    title = a_tag.get_text(strip=True)
                    links.append({"title": title, "url": full_url})
        return links
    except Exception as e:
        print(f"❌ 目录页请求失败: {e}")
        return []


def scrape_mca_article(url):
    """
    【阶段二】进入单篇文章详情页，提取干净的文本语料
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        # 【核心修复】：解决详情页的中文乱码问题
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'html.parser')
        clean_sentences = []

        # 提取正文常见的标签
        paragraphs = soup.find_all(['p', 'span', 'div', 'td'])

        for p in paragraphs:
            # 清洗各种恶心的空格和换行符
            text = p.get_text().replace('\xa0', '').replace('\u3000', '').replace('\n', '').replace('\r', '').strip()

            # 【核心过滤规则】：必须包含“动作词” + “行政区划单位”，且长度大于10
            if len(text) > 10 and re.search(r"(撤销|设立|更名|划归|并入)", text) and re.search(r"(省|市|区|县|乡|镇)",
                                                                                               text):
                if text not in clean_sentences:
                    clean_sentences.append(text)

        return clean_sentences
    except Exception as e:
        print(f"❌ 文章页请求失败: {e}")
        return []


# ================= 主程序执行 =================
if __name__ == "__main__":

    index_url = "http://xzqh.mca.gov.cn/description?dcpid=1"

    # 1. 抓取文章列表
    article_links = get_article_links(index_url)
    print(f"✅ 成功找到 {len(article_links)} 篇文章链接。")

    all_extracted_texts = []

    # 2. 遍历抓取详情
    # ⚠️ 注意：这里使用 article_links[:3] 表示只测试前 3 篇。
    # 验证没问题后，可以把 [:3] 删掉，执行全量抓取！
    for item in article_links:
        print(f"\n⏳ 正在抓取: {item['title']}")
        print(f"🔗 链接: {item['url']}")

        sentences = scrape_mca_article(item['url'])

        for text in sentences:
            all_extracted_texts.append({"source": item['title'], "raw_text": text})

        print(f"-> 本篇提取到 {len(sentences)} 条有效语料")

        # 必须加延时，防止高频访问被民政部网站封 IP！
        time.sleep(2)

    # 3. 结果汇总与保存
    if all_extracted_texts:
        df = pd.DataFrame(all_extracted_texts)
        print(f"\n🎉 大功告成！本次共抓取到 {len(df)} 条结构化变更语料。\n")

        # 在 Jupyter 中显示前 10 条
        display(df.head(10))

        # 【保存文件】：请修改为你的纯英文路径
        save_path = r"D:\code\mca_dynamic_changes.csv"
        # df.to_csv(save_path, index=False, encoding="utf-8-sig")
        print(f"💡 提示：取消上方代码的注释，即可将数据保存至 {save_path}")
    else:
        print("\n⚠️ 未能提取到有效文本，请检查网络或网站结构。")