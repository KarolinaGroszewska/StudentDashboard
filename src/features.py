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
    return summary

def calculate_risk_level(student_df: pd.DataFrame) -> float:
    avg_score = student_df["percent"].mean()
    missing_count = student_df[student_df["submitted"] == False].shape[0]

    risk_score = (100 - avg_score)
    return risk_score

def assign_risk_level(risk_score: float) -> str:
    if risk_score >= 40:
        return "High Risk"
    elif risk_score >= 35:
        return "Moderate Risk"
    else:
        return "Low Risk"
    
def add_risk_levels(student_summary: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    risk_scores = []

    for student_id in student_summary["student_id"]:
        student_df = df[df["student_id"] == student_id]
        risk_score = calculate_risk_level(student_df)
        risk_scores.append(risk_score)
    student_summary["risk_score"] = risk_scores
    student_summary["risk_level"] = student_summary["risk_score"].apply(assign_risk_level)
    return student_summary