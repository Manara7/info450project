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

st.sidebar.header("Filters")

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
col3.metric("Number of Individuals", f"{selected_count:,}")

st.subheader("Income Distribution for Selected Education Group")

income_bins = pd.cut(
    filtered_df["INCWAGE"],
    bins=20
)

income_distribution = (
    income_bins
    .value_counts()
    .sort_index()
    .reset_index()
)

income_distribution.columns = ["IncomeRange", "NumberOfIndividuals"]
income_distribution["IncomeRange"] = income_distribution["IncomeRange"].astype(str)

st.bar_chart(
    income_distribution,
    x="IncomeRange",
    y="NumberOfIndividuals"
)

st.subheader("Average Income by Education Level")

avg_income_df = (
    df.groupby("EducationGroup", observed=True)["INCWAGE"]
    .mean()
    .reindex(education_order)
    .reset_index()
)

avg_income_df.columns = ["EducationGroup", "AverageIncome"]

st.bar_chart(
    avg_income_df,
    x="EducationGroup",
    y="AverageIncome"
)


