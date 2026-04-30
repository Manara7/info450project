import streamlit as st
import pandas as pd
import altair as alt

st.title("Career Earnings and Work-Life Analysis")

st.write(
    "This app explores whether a bachelor's degree is enough to secure a substantial salary, "
    "or whether higher income levels are more associated with graduate education."
)
 st.write ( "Authors : ␣ Manara, ␣ Feaven , ␣ Caitlin ,  ␣ Justing" )

df = pd.read_csv("streamlit_data.csv")
df = df[df["INCWAGE"] > 0]

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

bins = list(range(0, 200001, 20000))
labels = [f"${bins[i]//1000}k-${bins[i+1]//1000}k" for i in range(len(bins)-1)]

filtered_df = filtered_df.copy()
filtered_df["Income Range"] = pd.cut(
    filtered_df["INCWAGE"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

income_distribution = (
    filtered_df["Income Range"]
    .value_counts()
    .sort_index()
    .reset_index()
)

income_distribution.columns = ["Income Range", "Number of Individuals"]

hist_chart = (
    alt.Chart(income_distribution)
    .mark_bar(color="#1f77b4")
    .encode(
        x=alt.X(
            "Income Range:N",
            title="Income Range",
            sort=labels,
            axis=alt.Axis(labelAngle=-35, labelColor="black", titleColor="black")
        ),
        y=alt.Y(
            "Number of Individuals:Q",
            title="Number of Individuals",
            axis=alt.Axis(labelColor="black", titleColor="black", grid=False)
        ),
        tooltip=["Income Range", "Number of Individuals"]
    )
    .properties(width=700, height=350, background="white")
    .configure_view(stroke=None)
)

st.altair_chart(hist_chart, use_container_width=True)

st.subheader("Average Income by Education Level")

avg_income_df = (
    df.groupby("EducationGroup", observed=True)["INCWAGE"]
    .mean()
    .reindex(education_order)
    .reset_index()
)

avg_income_df.columns = ["Education Group", "Average Income"]

bar_chart = (
    alt.Chart(avg_income_df)
    .mark_bar(color="#1f77b4")
    .encode(
        x=alt.X(
            "Education Group:N",
            sort=education_order,
            title="Education Level",
            axis=alt.Axis(labelAngle=-25, labelColor="black", titleColor="black")
        ),
        y=alt.Y(
            "Average Income:Q",
            title="Average Annual Income ($)",
            axis=alt.Axis(labelColor="black", titleColor="black", grid=False)
        ),
        tooltip=[
            "Education Group",
            alt.Tooltip("Average Income:Q", format="$,.0f")
        ]
    )
    .properties(width=700, height=350, background="white")
    .configure_view(stroke=None)
)

st.altair_chart(bar_chart, use_container_width=True)

st.write(
    "The dashboard shows that average income increases as education level rises. "
    "Graduate degree graduates have the highest average income, supporting the conclusion "
    "that higher education is associated with stronger earning potential."
)
