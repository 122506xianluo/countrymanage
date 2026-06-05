
import pandas as pd

def load_changes(path="data/changes.csv"):
    df = pd.read_csv(path)

    df = df.drop_duplicates()
    df = df.dropna()

    return df
