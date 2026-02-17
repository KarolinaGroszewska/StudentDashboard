import pandas as pd 

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["percent"] = df["score"] / df["max_score"] * 100
    df["is_missing"] = df["submitted"] == False
    return df

def get_student_summary(df):
    summary = df.groupby(["student_id", "student_name", "class_period"]).agg(
        avg_score=pd.NamedAgg(column="percent", aggfunc="mean"),
        total_assignments=pd.NamedAgg(column="assignment_type", aggfunc="count"),
        missing_assignments=pd.NamedAgg(column="is_missing", aggfunc="sum")
    ).reset_index()
    summary["at_risk"] = (summary["avg_score"] < 70) | (summary["missing_assignments"] > 2)
    return summary