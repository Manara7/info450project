import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Career Earnings and Work-Life Analysis")
st.write("This app explores whether a bachelor's degree is enough to secure a substantial salary.")

df = pd.read_csv("streamlit_data.csv")

selected_group = st.sidebar.selectbox(
    "Select an education group",
    sorted(df["EducationGroup"].dropna().unique())
)

st.subheader("Average Income by Education Group")
income_by_edu = df.groupby("EducationGroup")["INCWAGE"].mean().sort_values(ascending=False)

fig1, ax1 = plt.subplots()
income_by_edu.plot(kind="bar", ax=ax1)
ax1.set_title("Average Annual Income by Education Group")
ax1.set_xlabel("Education Group")
ax1.set_ylabel("Average Annual Income")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader(f"Income Distribution for {selected_group}")
filtered_df = df[df["EducationGroup"] == selected_group]

fig2, ax2 = plt.subplots()
filtered_df["INCWAGE"].plot(kind="hist", bins=30, ax=ax2)
ax2.set_title(f"Income Distribution: {selected_group}")
ax2.set_xlabel("Annual Income")
ax2.set_ylabel("Frequency")
st.pyplot(fig2)