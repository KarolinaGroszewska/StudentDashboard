import streamlit as st
import pandas as pd
import plotly.express as px

# Modules
from src.clean_data import clean_data
from src.features import add_features, get_student_summary
from src.analytics import class_performance, assignment_performance


st.set_page_config(
    page_title="Student Performance Dashboard", 
    layout="wide"
)

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/computer_science_teacher_dataset_2026.csv")
    df = clean_data(df)
    df = add_features(df)
    return df

df = load_data()
student_summary = get_student_summary(df)

st.title("Student Performance Dashboard")
st.header("Class Performance Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Students", student_summary.shape[0])
col2.metric("Average Score", f"{student_summary['avg_score'].mean():.2f}%")
col3.metric("At Risk Students", student_summary['at_risk'].sum())