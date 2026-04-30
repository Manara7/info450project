import streamlit as st
import pandas as pd

st.title("Career Earnings and Work-Life Analysis")

st.write(
    "This app explores whether a bachelor's degree is enough to secure a substantial salary, "
    "or whether higher income levels are more associated with graduate education."
)

df = pd.read_csv("streamlit_data.csv")

education_order = [
    "Less than High School",
    "High School",
    "Some College / Associate",
    "Bachelor's",
    "Graduate Degree"
]

df = df[df["EducationGroup"].isin(education_order)]

df["EducationGroup"] = pd.Categorical(
    df["EducationGroup"],
    categories=education_order,
    ordered=True
)

selected_group = st.sidebar.selectbox(
    "Select an education group",
    education_order
)

filtered_df = df[df["EducationGroup"] == selected_group]

st.subheader("Selected Education Group Summary")

selected_avg = filtered_df["INCWAGE"].mean()
selected_median = filtered_df["INCWAGE"].median()
selected_count = filtered_df.shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("Average Income", f"${selected_avg:,.0f}")
col2.metric("Median Income", f"${selected_median:,.0f}")
col3.metric("Individuals", f"{selected_count:,}")

st.subheader("Income Distribution for Selected Education Group")

income_distribution = (
    pd.cut(filtered_df["INCWAGE"], bins=20)
    .value_counts()
    .sort_index()
    .reset_index()
)

income_distribution.columns = ["Income Range", "Number of Individuals"]
income_distribution["Income Range"] = income_distribution["Income Range"].astype(str)

st.bar_chart(
    income_distribution,
    x="Income Range",
    y="Number of Individuals",
    color="#2196F3"
)

st.subheader("Average Income by Education Level")

avg_income_df = (
    df.groupby("EducationGroup", observed=True)["INCWAGE"]
    .mean()
    .reindex(education_order)
    .reset_index()
)

avg_income_df.columns = ["Education Group", "Average Income"]

st.bar_chart(
    avg_income_df,
    x="Education Group",
    y="Average Income",
    color="#4CAF50"
)

st.write(
    "The dashboard shows that average income increases as education level rises. "
    "Graduate degree graduates have the highest average income, which supports the finding "
    "that higher education is associated with stronger earning potential."
)
