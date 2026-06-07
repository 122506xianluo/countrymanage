
from flask import Flask, render_template
from src.data_clean import load_changes
from src.ner import extract_entities
from src.relation import extract_relations
from src.classify import classify_text
from src.graph import build_graph
from src.forecast import create_forecast_plot

app = Flask(__name__)

df = load_changes()

all_relations = []

for text in df["raw_text"]:

    relations = extract_relations(str(text))

    all_relations.extend(relations)

build_graph(all_relations)

create_forecast_plot(df["raw_text"])

@app.route("/")
def home():

    sample = str(df.iloc[0]["raw_text"])

    ner_result = extract_entities(sample)

    category = classify_text(sample)

    return render_template(
        "index.html",
        total=len(df),
        sample=sample,
        ner=ner_result,
        category=category,
        relation_count=len(all_relations)
    )

@app.route("/graph")
def graph():
    return render_template("graph.html")

if __name__ == "__main__":
    app.run(debug=True)
