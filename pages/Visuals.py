# This creates the page for displaying data visualizations.

import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
import json
import statistics
import matplotlib.pyplot as plt

with open("data.json", "r") as file:
    data = json.load(file)

car_names = []
car_speeds = []

for item in data["data_points"]:
    car_names.append(item["label"])
    car_speeds.append(item["value"])

fig, ax = plt.subplots()
ax.bar(car_names, car_speeds, color="navy")

ax.set_title(data["chart_title"])
ax.set_xlabel("Car Name")
ax.set_ylabel("Top Speed (km/h)")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)

st.subheader("Explore Car Speeds")

if "selected_cars" not in st.session_state:
    st.session_state.selected_cars = [
        item["label"] for item in data["data_points"]
    ]

selected_cars = st.multiselect(
    "Choose cars to compare:",
    [item["label"] for item in data["data_points"]],
    default=st.session_state.selected_cars
)

st.session_state.selected_cars = selected_cars

dynamic_names = []
dynamic_speeds = []

for item in data["data_points"]:
    if item["label"] in st.session_state.selected_cars:
        dynamic_names.append(item["label"])
        dynamic_speeds.append(item["value"])

fig2, ax2 = plt.subplots()
ax2.plot(dynamic_names, dynamic_speeds, color="darkorange", marker="o")

ax2.set_title("Selected Cars: Top Speeds")
ax2.set_xlabel("Car Name")
ax2.set_ylabel("Top Speed (km/h)")

plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
fig2.tight_layout()

st.pyplot(fig2)
# EXTRA CREDIT: mean and median of selected cars
if len(dynamic_speeds) > 0:
    current_mean = statistics.mean(dynamic_speeds)
    current_median = statistics.median(dynamic_speeds)
else:
    current_mean = 0
    current_median = 0

if "prev_mean" not in st.session_state:
    st.session_state.prev_mean = current_mean
    st.session_state.prev_median = current_median

col1, col2 = st.columns(2)
col1.metric(
    "Mean Top Speed (km/h)",
    round(current_mean, 1),
    delta=round(current_mean - st.session_state.prev_mean, 1)
)
col2.metric(
    "Median Top Speed (km/h)",
    round(current_median, 1),
    delta=round(current_median - st.session_state.prev_median, 1)
)

st.session_state.prev_mean = current_mean
st.session_state.prev_median = current_median

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
import pandas as pd

st.header("Survey Results: Car Brands & Driving Time")

df = pd.read_csv("data.csv")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
df = df.dropna()
df["Category"] = df["Category"].str.strip()

# STATIC CHART: pie chart of favorite brands
brand_counts = df["Category"].value_counts()

fig3, ax3 = plt.subplots()
ax3.pie(brand_counts.values, labels=brand_counts.index, autopct="%1.0f%%")
ax3.set_title("Favorite Car Brands (Survey)")
st.pyplot(fig3)

# DYNAMIC CHART: scatter plot filtered by a slider
if "min_hours" not in st.session_state:
    st.session_state.min_hours = 0

min_hours = st.slider(
    "Show people who drive at least this many hours a week:",
    0, int(df["Value"].max()),
    st.session_state.min_hours
)
st.session_state.min_hours = min_hours

filtered = df[df["Value"] >= min_hours]

fig4, ax4 = plt.subplots()
ax4.scatter(filtered["Category"], filtered["Value"], color="seagreen")
ax4.set_title("Weekly Driving Hours by Favorite Brand")
ax4.set_xlabel("Car Brand")
ax4.set_ylabel("Hours Driven per Week")
plt.setp(ax4.get_xticklabels(), rotation=45, ha="right")
fig4.tight_layout()
st.pyplot(fig4)

# EXTRA CREDIT: mean and median of filtered survey data
if len(filtered) > 0:
    survey_mean = statistics.mean(filtered["Value"])
    survey_median = statistics.median(filtered["Value"])
else:
    survey_mean = 0
    survey_median = 0

if "prev_survey_mean" not in st.session_state:
    st.session_state.prev_survey_mean = survey_mean
    st.session_state.prev_survey_median = survey_median

col3, col4 = st.columns(2)
col3.metric(
    "Mean Hours Driven",
    round(survey_mean, 1),
    delta=round(survey_mean - st.session_state.prev_survey_mean, 1)
)
col4.metric(
    "Median Hours Driven",
    round(survey_median, 1),
    delta=round(survey_median - st.session_state.prev_survey_median, 1)
)

st.session_state.prev_survey_mean = survey_mean
st.session_state.prev_survey_median = survey_median
