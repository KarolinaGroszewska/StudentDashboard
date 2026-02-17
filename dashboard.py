import streamlit as st
import pandas as pd
import plotly.express as px

# Modules
from src.clean_data import clean_data
from src.features import add_features, add_risk_levels, get_student_summary
from src.analytics import class_performance, assignment_performance, class_trends


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
student_summary = add_risk_levels(student_summary, df)

st.title("Student Performance Dashboard")
st.header("Class Performance Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", student_summary.shape[0])
col2.metric("Average Score", f"{student_summary['avg_score'].mean():.2f}%")
col3.metric("High Risk Students", student_summary[student_summary["risk_level"] == "High Risk"].shape[0])
col4.metric("Moderate Risk Students", student_summary[student_summary["risk_level"] == "Moderate Risk"].shape[0])

# Individual Student Performance
st.header("Individual Student Performance")

# student= st.selectbox("Select Student Name", student_summary.sort_values("student_name")["student_name"].unique())
# student_df = df[df["student_name"] == student]
student_summary["display_name"] = student_summary["student_name"] + " [ID: " + student_summary["student_id"].astype(str) + "]"
selected_display = st.selectbox(
    "Select Student",
    student_summary.sort_values("student_name")["display_name"]
)
selected_student_id = student_summary[
    student_summary["display_name"] == selected_display
]["student_id"].iloc[0]
student_df = df[df["student_id"] == selected_student_id]

student_name = student_df["student_name"].iloc[0]
class_period = student_df["class_period"].iloc[0]

avg_score = student_df["percent"].mean()
#TODO: check this line if broken
missing_count = student_df[student_df["submitted"] == False].shape[0]
assignment_count = student_df.shape[0]

student_row = student_summary[student_summary["student_id"] == selected_student_id].iloc[0]
risk_level = student_row["risk_level"]
st.subheader(f"Performance Summary for {student_name} (Class Period: {class_period})")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Score", f"{avg_score:.2f}%")
col2.metric("Assignments Submitted", f"{assignment_count - missing_count} / {assignment_count}")
col3.metric("Missing Assignments", missing_count)
col4.metric("Risk Level", risk_level)

st.subheader(f"Assignment Details for {student_summary[student_summary['student_id'] == selected_student_id]['student_name'].iloc[0]}")

student_table = student_df[
    [
        "date",
        "assignment_name",
        "assignment_type",
        "percent"
    ]
].sort_values("date", ascending=False)

student_table["percent"] = student_table["percent"].round(2)
student_table["date"] = pd.to_datetime(student_table["date"]).dt.strftime("%m-%d-%Y")

student_table = student_table.rename(columns={
    "date": "Date",
    "assignment_name": "Assignment Name",
    "assignment_type": "Assignment Type",
    "percent": "Score (%)"
})

st.dataframe(student_table, use_container_width=True)

st.subheader(f"Performance over Time for {student_summary[student_summary['student_id'] == selected_student_id]['student_name'].iloc[0]}")

student_df = student_df.sort_values("date")
student_df["rolling_avg"] = student_df["percent"].rolling(window=3, min_periods=1).mean()

fig_student = px.scatter(
    student_df,
    x="date",
    y="percent",
    color="assignment_type",
    symbol="assignment_type",
    hover_data=["assignment_name", "percent"],
    title=f"Performance of {student_summary[student_summary['student_id'] == selected_student_id]['student_name'].iloc[0]} Over Time",
    labels={"date": "Date", "percent": "Score (%)"}
)

fig_student.add_scatter(
    x = student_df["date"],
    y = student_df["rolling_avg"],
    mode="lines",
    name="Rolling Average (3 Assignments)",
    line=dict(color="white", dash="dash", width=2)
)

fig_student.update_layout(
    yaxis = dict(range=[-5, 105]),
    xaxis_title="Date",
    yaxis_title="Score (%)",
    legend_title="Assignment Type",
)
st.plotly_chart(fig_student, use_container_width=True)



# st.header("Class Performance by Period")
# class_perf = class_performance(df)
# fig_class = px.bar(
#     class_perf,
#     x="class_period",
#     y="avg_score",
#     title="Average Performance by Class Period",
#     labels={"class_period": "Class Period", "avg_score": "Average Score (%)"},
#     text_auto=".2f",
#     color="class_period",  # Use class_period for color differentiation
#     color_discrete_sequence=px.colors.qualitative.Plotly  # Set a color sequence
# )
# st.plotly_chart(fig_class, use_container_width=True)

# trend_df = class_trends(df)
# fig_trend = px.line(
#     trend_df,
#     x="date",
#     y="avg_score",
#     color="class_period",
#     color_discrete_sequence=px.colors.qualitative.Plotly,
#     title="Class Performance Trends Over Time",
#     labels={"date": "Date", "avg_score": "Average Score (%)", "class_period": "Class Period"}
# )
# fig_trend.update_layout(
#     yaxis=dict(range=[-5, 105]),
#     xaxis_title="Date",
#     yaxis_title="Average Score (%)",
#     legend_title="Class Period"
# )
# st.plotly_chart(fig_trend, use_container_width=True)

# st.header("Assignment Performance by Type")
# assignment_perf = assignment_performance(df)
# fig_assignment = px.bar(
#     assignment_perf,
#     x="assignment_type",
#     y="avg_score",
#     title="Average Performance by Assignment Type",
#     labels={"assignment_type": "Assignment Type", "avg_score": "Average Score (%)"},
#     text_auto=".2f",
#     color="assignment_type",  # Use assignment_type for color differentiation
#     color_discrete_sequence=px.colors.qualitative.Plotly  # Set a color sequence
# )
# st.plotly_chart(fig_assignment, use_container_width=True)

# st.header("Raw Student Data")
# with st.expander("Show Raw Data"):
#     st.dataframe(df)
