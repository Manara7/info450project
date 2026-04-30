import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Career Earnings Dashboard", layout="wide")

st.title("Career Earnings and Work-Life Analysis")

st.write(
    "This app explores whether a bachelor's degree is enough to secure a substantial salary, "
    "or whether higher income levels are associated with advanced education."
)

df = pd.read_csv("streamlit_data.csv")

education_order = [
    "Less than High School",
    "High School Diploma",
    "Some College / Associate",
    "Bachelor's Degree",
    "Advanced Degree"
]

# Keep only valid groups
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

col1.metric("Average Income", f"${filtered_df['INCWAGE'].mean():,.0f}")
col2.metric("Median Income", f"${filtered_df['INCWAGE'].median():,.0f}")
col3.metric("Number of Records", f"{len(filtered_df):,}")
st.subheader(f"Income Distribution for {selected_group}")

fig1, ax1 = plt.subplots()

ax1.hist(filtered_df["INCWAGE"], bins=30)

ax1.set_xlabel("Annual Income ($)")
ax1.set_ylabel("Count")
ax1.set_title("Income Distribution")

st.pyplot(fig1)

st.markdown("""
This chart shows how income is distributed within the selected education group.
It helps identify whether most individuals earn lower, middle, or higher incomes.
""")

st.subheader("Average Income by Education Level")

avg_income = (
    df.groupby("EducationGroup", observed=True)["INCWAGE"]
    .mean()
    .reindex(education_order)
)

fig2, ax2 = plt.subplots()

ax2.bar(avg_income.index.astype(str), avg_income.values)

ax2.set_xlabel("Education Level")
ax2.set_ylabel("Average Income ($)")
ax2.set_title("Average Income by Education Level")

plt.xticks(rotation=25)

st.pyplot(fig2)

st.markdown("""
This chart compares average income across all education levels.
It helps determine whether a bachelor's degree is sufficient or if advanced degrees lead to higher earnings.
""")

if "HighEarner" in df.columns:

    st.subheader("High Earner Rate by Education Level")

    high_rate = (
        df.groupby("EducationGroup", observed=True)["HighEarner"]
        .mean()
        .reindex(education_order)
    )

    fig3, ax3 = plt.subplots()

    ax3.bar(high_rate.index.astype(str), high_rate.values * 100)

    ax3.set_xlabel("Education Level")
    ax3.set_ylabel("High Earner %")
    ax3.set_title("Percent of High Earners")

    plt.xticks(rotation=25)

    st.pyplot(fig3)
st.subheader("Data Preview")
st.dataframe(filtered_df.head())
