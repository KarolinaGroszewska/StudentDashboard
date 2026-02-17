import streamlit as st
import pandas as pd
import plotly.express as px

# Modules
from src.clean_data import clean_data
from src.features import add_features, add_risk_levels, get_student_summary

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

st.subheader("Performance by Assignment Type")

type_perf = (
    student_df.groupby("assignment_type")["percent"]
    .mean()
    .reset_index()
)

fig_type = px.bar(
    type_perf,
    x="assignment_type",
    y="percent",
    title="Average Score by Assignment Type",
    color="assignment_type",
    labels={"percent": "Average Score"}
)

st.plotly_chart(fig_type, use_container_width=True)

st.subheader("Recent Performance Trends")
recent_df = student_df.sort_values("date", ascending=False).head(10)
recent_df["date"] = pd.to_datetime(recent_df["date"]).dt.strftime("%m-%d-%Y")
recent_avg = recent_df["percent"].mean()
overall_avg = student_df["percent"].mean()
diff = recent_avg - overall_avg
if diff > 5:
    st.success(f"Recent performance is improving! Recent Avg: {recent_avg:.2f}% vs Overall Avg: {overall_avg:.2f}%")
elif diff < -5:
    st.warning(f"Recent performance is declining. Recent Avg: {recent_avg:.2f}% vs Overall Avg: {overall_avg:.2f}%")
else:
    st.info(f"Recent performance is stable. Recent Avg: {recent_avg:.2f}% vs Overall Avg: {overall_avg:.2f}%")


st.subheader("Missing Assignments")

missing_df = student_df[student_df["is_missing"] == True]

if missing_df.empty:

    st.success("No missing assignments!")

else:
    missing_df["date"] = pd.to_datetime(missing_df["date"]).dt.strftime("%m-%d-%Y")
    missing_table = missing_df[
        [
            "date",
            "assignment_name",
            "assignment_type"
        ]
    ].sort_values("date")

    missing_table = missing_table.rename(columns={
        "date": "Date",
        "assignment_name": "Assignment",
        "assignment_type": "Type"
    })

    st.dataframe(missing_table, use_container_width=True)

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