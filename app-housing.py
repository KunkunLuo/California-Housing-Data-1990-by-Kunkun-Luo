import streamlit as st
import pandas as pd

# ---------- 标题（已换成你的名字） ----------
st.title("California Housing Data (1990) by Kunkun Luo")

# ---------- 读取数据 ----------
@st.cache_data
def load_data():
    return pd.read_csv("housing.csv")

df = load_data()

# ---------- 滑块：最小房价中位数 ----------
min_value = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000,
    step=1000
)

# ---------- 副标题 ----------
st.subheader("See more filters in the sidebar:")

# ---------- 侧边栏：地点类型多选 ----------
all_locations = ["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"]
selected_locations = st.sidebar.multiselect(
    "Choose the location type",
    options=all_locations,
    default=all_locations
)

# ---------- 侧边栏：收入等级单选（默认 High） ----------
income_level = st.sidebar.radio(
    "Choose income level",
    options=["Low", "Medium", "High"],
    index=2
)

# ---------- 数据筛选 ----------
# 1) 房价筛选
filtered = df[df["median_house_value"] >= min_value].copy()

# 2) 地点类型筛选
filtered = filtered[filtered["ocean_proximity"].isin(selected_locations)]

# 3) 收入等级筛选
if income_level == "Low":
    filtered = filtered[filtered["median_income"] <= 2.5]
elif income_level == "Medium":
    filtered = filtered[(filtered["median_income"] > 2.5) & (filtered["median_income"] < 4.5)]
elif income_level == "High":
    filtered = filtered[filtered["median_income"] >= 4.5]

# ---------- 地图 ----------
if filtered.empty:
    st.warning("No districts match the current filters. Try lowering the house value or changing the income level.")
else:
    st.map(filtered, latitude="latitude", longitude="longitude")

# ---------- 直方图 ----------
st.subheader("Histogram of Median House Value")

if not filtered.empty:
    hist_data = pd.cut(filtered["median_house_value"], bins=30).value_counts().sort_index()
    hist_df = hist_data.reset_index()
    hist_df.columns = ["Price Range", "Count"]
    hist_df["Price Range"] = hist_df["Price Range"].astype(str)
    st.bar_chart(hist_df, x="Price Range", y="Count", use_container_width=True)
