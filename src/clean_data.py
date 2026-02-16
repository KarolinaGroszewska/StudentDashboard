import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["score"] = df["score"].fillna(0)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["max_score"] = df["max_score"].astype(float)
    df["class_period"] = df["class_period"].astype(int)
    return df