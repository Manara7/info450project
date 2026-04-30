import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Career Earnings and Work-Life Analysis")
st.write("This app explores whether a bachelor's degree is enough to secure a substantial salary.")

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

selected_group = st.sidebar.selectbox(
    "Select an education group",
    education_order
)

filtered_df = df[df["EducationGroup"] == selected_group]

st.subheader("Average Income for Selected Education Group")

selected_avg = filtered_df["INCWAGE"].mean()

st.metric(
    label=f"Average Income: {selected_group}",
    value=f"${selected_avg:,.0f}"
)

st.subheader("Income Distribution for Selected Education Group")

fig, ax = plt.subplots(figsize=(10, 5))

ax.hist(filtered_df["INCWAGE"], bins=30)

ax.set_title(f"Income Distribution for {selected_group}")
ax.set_xlabel("Annual Income ($)")
ax.set_ylabel("Number of People")

st.pyplot(fig)

st.subheader("Average Income by Education Level")

avg_income = (
    df.groupby("EducationGroup", observed=True)["INCWAGE"]
    .mean()
    .reindex(education_order)
)

fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.bar(avg_income.index.astype(str), avg_income.values)

ax2.set_title("Average Income by Education Level")
ax2.set_xlabel("Education Level")
ax2.set_ylabel("Average Annual Income ($)")
ax2.tick_params(axis="x", rotation=25)

st.pyplot(fig2)
