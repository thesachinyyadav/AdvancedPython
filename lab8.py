import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Traffic Data Explorer", layout="wide")
st.title("Traffic Data Explorer")

st.sidebar.header("Load data")
upload = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
path = st.sidebar.text_input("Or enter CSV path:", "")

df = None
if upload is not None:
    df = pd.read_csv(upload)
elif path.strip() != "":
    df = pd.read_csv(path.strip())
else:
    st.info("Upload a CSV file or enter a path to start.")

if df is not None:
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    
    st.header("A. Aggregations")

    if "traffic_volume" in df.columns and "timestamp" in df.columns:
        daily_volume = df.groupby(df["timestamp"].dt.date)["traffic_volume"].sum()
        hourly_volume = df.groupby(df["timestamp"].dt.hour)["traffic_volume"].sum()

        st.subheader("Total Traffic Volume per Day")
        st.dataframe(daily_volume.reset_index().rename(columns={"timestamp":"date","traffic_volume":"daily_volume"}))
        st.line_chart(daily_volume)

        st.subheader("Total Traffic Volume per Hour")
        st.dataframe(hourly_volume.reset_index().rename(columns={"timestamp":"hour","traffic_volume":"hourly_volume"}))
        st.bar_chart(hourly_volume)

    if "location_id" in df.columns and "avg_vehicle_speed" in df.columns:
        avg_speed_per_zone = df.groupby("location_id")["avg_vehicle_speed"].mean()
        st.subheader("Average Speed per Location/Zone")
        st.dataframe(avg_speed_per_zone.reset_index().rename(columns={"avg_vehicle_speed":"avg_speed"}))

    if "traffic_volume" in df.columns and "timestamp" in df.columns:
        peak_hours = st.multiselect("Select Peak Hours", options=list(range(24)), default=[7,8,9,16,17,18,19])
        peak_df = df[df["timestamp"].dt.hour.isin(peak_hours)]
        if not peak_df.empty:
            st.write("Max traffic at peak hours:", int(peak_df["traffic_volume"].max()))
            st.write("Min traffic at peak hours:", int(peak_df["traffic_volume"].min()))

    if all(x in df.columns for x in ["vehicle_count_cars","vehicle_count_trucks","vehicle_count_bikes"]):
        df["total_vehicle_count"] = df["vehicle_count_cars"] + df["vehicle_count_trucks"] + df["vehicle_count_bikes"]
        st.write("Total Vehicle Count across dataset:", int(df["total_vehicle_count"].sum()))

    st.header("B. Comparisons, Masks, and Boolean Arrays")

    if "traffic_volume" in df.columns:
        threshold = st.slider("Traffic Volume Threshold", int(df["traffic_volume"].min()), int(df["traffic_volume"].max()), step=100)
        mask = df["traffic_volume"] > threshold
        st.write("Rows with traffic_volume >", threshold)
        st.dataframe(df[mask].head(20))

    if "timestamp" in df.columns:
        df["weekday"] = df["timestamp"].dt.weekday
        weekdays = df[df["weekday"] < 5]
        weekends = df[df["weekday"] >= 5]
        st.subheader("Weekdays vs Weekends")
        st.write("Weekday rows:", len(weekdays))
        st.write("Weekend rows:", len(weekends))

    if "location_id" in df.columns:
        locs = df["location_id"].unique().tolist()
        selected = st.multiselect("Filter by Location", options=locs)
        if selected:
            st.dataframe(df[df["location_id"].isin(selected)].head(20))

    st.header("C. Sorting Arrays")

    if "traffic_volume" in df.columns:
        sorted_by_vol = df.sort_values("traffic_volume", ascending=False)
        st.subheader("Top 20 busiest times (by traffic_volume)")
        st.dataframe(sorted_by_vol.head(20))

    if "timestamp" in df.columns:
        sorted_by_time = df.sort_values("timestamp")
        st.subheader("Data sorted by date/time")
        st.dataframe(sorted_by_time.head(20))

    if "location_id" in df.columns and "traffic_volume" in df.columns:
        sorted_by_loc_vol = df.sort_values(["location_id","traffic_volume"], ascending=[True,False])
        st.subheader("Data sorted by Location then Volume")
        st.dataframe(sorted_by_loc_vol.head(20))
