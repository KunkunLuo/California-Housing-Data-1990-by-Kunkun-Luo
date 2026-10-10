from pathlib import Path

import streamlit as st
import pandas as pd
from matplotlib import style
from matplotlib.figure import Figure

style.use("seaborn-v0_8")

st.title("California Housing Data (1990) by Kunkun Luo")

# The CSV stays in the repository root, including when this page is in pages/.
app_folder = Path(__file__).resolve().parent
data_folder = app_folder.parent if app_folder.name == "pages" else app_folder
df = pd.read_csv(data_folder / "housing.csv")

house_value_filter = st.slider(
    "Minimal Median House Value", 0, 500001, 200000
)

st.subheader("See more filters in the sidebar:")

location_types = df["ocean_proximity"].dropna().unique().tolist()
location_filter = st.sidebar.multiselect(
    "Choose the location type", location_types, default=location_types
)

income_filter = st.sidebar.radio(
    "Choose income level", ["Low", "Medium", "High"]
)

df = df[df["median_house_value"] >= house_value_filter]
df = df[df["ocean_proximity"].isin(location_filter)]

if income_filter == "Low":
    df = df[df["median_income"] <= 2.5]
elif income_filter == "Medium":
    df = df[(df["median_income"] > 2.5) & (df["median_income"] < 4.5)]
else:
    df = df[df["median_income"] >= 4.5]

if df.empty:
    st.info("No districts match these filters. Try adjusting your selections.")
    st.stop()

st.map(df[["latitude", "longitude"]])

st.subheader("Median House Value Distribution")
fig = Figure(figsize=(10, 5))
ax = fig.subplots()
ax.hist(df["median_house_value"], bins=30)
ax.set_xlabel("Median House Value (USD)")
ax.set_ylabel("Number of Districts")
st.pyplot(fig)
