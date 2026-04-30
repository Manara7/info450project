import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(page_title="Career Earnings Dashboard", layout="wide")

st.title("Career Earnings and Work-Life Analysis")

st.write(
    "This app explores whether a bachelor's degree is enough to secure a substantial salary, "
    "or whether higher income levels are more associated with advanced education."
)


df = pd.read_csv("streamlit_data.csv")


education_order = [
    "Less than High School",
    "High School Diploma",
    "Some College / Associate",
    "Bachelor's Degree",
    "Advanced Degree"
]

df = df[df["EducationGroup"].isin(education_order)]

df["EducationGroup"] = pd.Categorical(
    df["EducationGroup"],
    categories=education_order,
    ordered=True
)

st.sidebar.header("Filter Options")

selected_group = st.sidebar.selectbox(
    "Select an education group",
    education_order
)

filtered_df = df[df["EducationGroup"] == selected_group]


st.subheader("Summary for Selected Education Group")

col1, col2, col3 = st.columns(3)

selected_avg = filtered_df["INCWAGE"].mean()
selected_median = filtered_df["INCWAGE"].median()
selected_count = len(filtered_df)

col1.metric("Average Income", f"${selected_avg:,.0f}")
col2.metric("Median Income", f"${selected_median:,.0f}")
col3.metric("Number of Records", f"{selected_count:,}")



st.subheader(f"Income Distribution for {selected_group}")

fig1, ax1 = plt.subplots(figsize=(10, 5))

ax1.hist(filtered_df["INCWAGE"], bins=30)

ax1.set_title(f"Income Distribution: {selected_group}")
ax1.set_xlabel("Annual Income ($)")
ax1.set_ylabel("Number of Individuals")

plt.tight_layout()
st.pyplot(fig1)

st.markdown(
    "This chart shows how income is distributed within the selected education group. "
    "It helps show whether most people in that group earn lower, middle, or higher incomes."

st.subheader("Average Income by Education Level")

avg_income_by_education = (
    df.groupby("EducationGroup", observed=True)["INCWAGE"]
    .mean()
    .reindex(education_order)
)

fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.bar(
    avg_income_by_education.index.astype(str),
    avg_income_by_education.values
)

ax2.set_title("Average Annual Income by Education Level")
ax2.set_xlabel("Education Level")
ax2.set_ylabel("Average Annual Income ($)")
ax2.tick_params(axis="x", rotation=25)

plt.tight_layout()
st.pyplot(fig2)

st.markdown(
    "This chart compares average income across education levels in order. "
    "It directly supports the project question by showing whether bachelor's degree holders "
    "earn less, about the same, or more than advanced degree holders."
)


if "HighEarner" in df.columns:
    st.subheader("High Earner Rate by Education Level")

    high_earner_rate = (
        df.groupby("EducationGroup", observed=True)["HighEarner"]
        .mean()
        .reindex(education_order)
    )

    fig3, ax3 = plt.subplots(figsize=(10, 5))

    ax3.bar(
        high_earner_rate.index.astype(str),
        high_earner_rate.values * 100
    )

    ax3.set_title("Percent of High Earners by Education Level")
    ax3.set_xlabel("Education Level")
    ax3.set_ylabel("High Earner Rate (%)")
    ax3.tick_params(axis="x", rotation=25)

    plt.tight_layout()
    st.pyplot(fig3)

    st.markdown(
        "This chart shows the percent of people in each education group who earn above the median income. "
        "This is useful because the project is not only looking at average income, but also who is more likely "
        "to be classified as a high earner."
    )

st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head())
