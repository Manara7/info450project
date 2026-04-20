import streamlit as st
import pandas as pd

st.title("Career Earnings and Work-Life Analysis")
st.write("This app explores whether a bachelor's degree is enough to secure a substantial salary.")

df = pd.read_csv("streamlit_data.csv")

selected_group = st.sidebar.selectbox(
    "Select an education group",
    sorted(df["EducationGroup"].dropna().unique())
)

st.subheader("Average Income for Selected Education Group")
selected_avg = df[df["EducationGroup"] == selected_group]["INCWAGE"].mean()
st.metric(label=f"Average Income: {selected_group}", value=f"${selected_avg:,.0f}")

st.subheader("Income Distribution for Selected Education Group")
filtered_df = df[df["EducationGroup"] == selected_group]
hist_data = filtered_df["INCWAGE"].value_counts(bins=30).sort_index()
st.bar_chart(hist_data)
