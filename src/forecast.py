
import matplotlib.pyplot as plt
from collections import Counter
import re

def create_forecast_plot(texts):

    years = []

    for text in texts:

        matches = re.findall(r"(20\d{2})年", str(text))

        years.extend(matches)

    counter = Counter(years)

    x = sorted(counter.keys())
    y = [counter[i] for i in x]

    plt.figure(figsize=(8,5))

    plt.plot(x, y, marker="o")

    plt.title("行政区划变更时间统计")
    plt.xlabel("Year")
    plt.ylabel("Count")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("static/forecast.png")
