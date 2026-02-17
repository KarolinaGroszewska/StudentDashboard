import pandas as pd

# TODO: Verify updated analytics code works with dashboard
def class_performance(df: pd.DataFrame) -> pd.DataFrame:
    performance = df.groupby("class_period").agg(
        avg_score=pd.NamedAgg(column="percent", aggfunc="mean"),
        total_students=pd.NamedAgg(column="student_id", aggfunc="nunique"),
        at_risk_students=pd.NamedAgg(column="at_risk", aggfunc="sum")
    ).reset_index()
    return performance

def assignment_performance(df: pd.DataFrame) -> pd.DataFrame:
    performance = df.groupby("assignment_type").agg(
        avg_score=pd.NamedAgg(column="percent", aggfunc="mean"),
        total_submissions=pd.NamedAgg(column="student_id", aggfunc="count"),
        missing_submissions=pd.NamedAgg(column="is_missing", aggfunc="sum")
    ).reset_index()
    return performance