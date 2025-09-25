import numpy as np
import pandas as pd
import streamlit as st

file_path = "Schaefer2018_600Parcels_gyrification266.csv"
data = pd.read_csv(file_path, header=None)

# Convert all to numeric and drop fully empty rows/columns
data = data.apply(pd.to_numeric, errors='coerce')
data = data.dropna(how="all", axis=0).dropna(how="all", axis=1)

data_array = data.values

# Extract subset
subset_array = data_array[25:75, :100]

# Full dataset stats
mean_val = np.nanmean(data_array)
median_val = np.nanmedian(data_array)
std_val = np.nanstd(data_array)

# Subset stats (fixed variable name)
subset_mean = np.nanmean(subset_array)
subset_median = np.nanmedian(subset_array)
subset_std = np.nanstd(subset_array)

# Streamlit App
st.title("Dataset Analysis with NumPy")

st.header("Task 1: Subset Information")
st.write("Shape of extracted subset:", subset_array.shape)

st.header("Task 2: Statistical Results")

st.subheader("Full Dataset")
st.write("Mean:", mean_val)
st.write("Median:", median_val)
st.write("Standard Deviation:", std_val)

st.subheader("Subset (50×100 slice)")
st.write("Mean:", subset_mean)
st.write("Median:", subset_median)
st.write("Standard Deviation:", subset_std)

st.header("Visualization")
st.line_chart(subset_array[:10])
