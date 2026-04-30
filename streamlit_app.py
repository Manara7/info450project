import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

max_income = st.sidebar.slider(
    "Maximum income shown",
    min_value=25000,
    max_value=200000,
    value=200000,
    step=5000
)

filtered_df = df[
    (df["EducationGroup"] == selected_group) &
    (df["INCWAGE"] <= max_income)
]

st.subheader("Selected Education Group Summary")

selected_avg = filtered_df["INCWAGE"].mean()
selected_median = filtered_df["INCWAGE"].median()
selected_count = filtered_df.shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("Average Income", f"${selected_avg:,.0f}")
col2.metric("Median Income", f"${selected_median:,.0f}")
col3.metric("Number of Individuals", f"{selected_count:,}")

st.subheader("Income Distribution for Selected Education Group")

fig, ax = plt.subplots(figsize=(10, 5))

ax.hist(
    filtered_df["INCWAGE"],
    bins=30,
    color="steelblue",
    edgecolor="black"
)

ax.set_title(f"Income Distribution for {selected_group}")
ax.set_xlabel("Annual Income ($)")
ax.set_ylabel("Number of Individuals")

st.pyplot(fig)

st.subheader("Average Income by Education Level")

avg_income = (
    df[df["INCWAGE"] <= max_income]
    .groupby("EducationGroup", observed=True)["INCWAGE"]
    .mean()
    .reindex(education_order)
)

fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.bar(
    avg_income.index.astype(str),
    avg_income.values,
    color="steelblue",
    edgecolor="black"
)

ax2.set_title("Average Income by Education Level")
ax2.set_xlabel("Education Level")
ax2.set_ylabel("Average Annual Income ($)")
ax2.tick_params(axis="x", rotation=25)

st.pyplot(fig2)

