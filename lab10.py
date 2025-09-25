import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

st.set_page_config(page_title="Phenotypic Data Analysis", layout="wide")

st.title("Phenotypic Data Analysis with NumPy & Pandas")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset successfully loaded!")

    st.subheader("Dataset Overview")
    st.write("**Shape of Dataset:**", df.shape)
    st.write("**Column Names:**", df.columns.tolist())
    
    st.write("**First 5 Rows:**")
    st.dataframe(df.head())

    st.write("**Last 5 Rows:**")
    st.dataframe(df.tail())

    st.write("**Description (Numeric & Categorical):**")
    st.dataframe(df.describe(include="all").transpose())

    st.subheader("Handling Missing Values")

    missing_info = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df)) * 100
    missing_df = pd.DataFrame({
        "Missing Count": missing_info,
        "Missing %": missing_percent
    })
    st.write("**Missing Value Summary:**")
    st.dataframe(missing_df)

    df = df.dropna(axis=1, thresh=len(df) * 0.5)

    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].mean())

    st.success("Missing values handled (columns >50% missing dropped, others filled with mean).")

    st.subheader("Data Conversion")

    id_cols = [col for col in df.columns if "id" in col.lower()]

    if id_cols:
        id_col = id_cols[0]
        df["numeric_Id"] = df[id_col].astype(str).str.extract("(\d+)").astype(float)
        st.success(f"Extracted numeric IDs from column: **{id_col}**")
        st.dataframe(df[[id_col, "numeric_Id"]].head())
    else:
        st.warning("No column containing 'id' found in dataset.")

    st.subheader("Data Standardization")

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "numeric_Id" in num_cols:
        num_cols.remove("numeric_Id")

    if num_cols:
        scaler = StandardScaler()
        df_zscore = df.copy()
        df_zscore[num_cols] = scaler.fit_transform(df[num_cols])

        minmax_scaler = MinMaxScaler()
        df_minmax = df.copy()
        df_minmax[num_cols] = minmax_scaler.fit_transform(df[num_cols])

        st.write("**Z-score Normalized Data (first 5 rows):**")
        st.dataframe(df_zscore.head())

        st.write("**Min-Max Scaled Data (first 5 rows):**")
        st.dataframe(df_minmax.head())

        st.download_button("Download Z-score Normalized CSV", df_zscore.to_csv(index=False), "phenotypic_zscore.csv", "text/csv")
        st.download_button("Download Min-Max Scaled CSV", df_minmax.to_csv(index=False), "phenotypic_minmax.csv", "text/csv")
    else:
        st.warning("No numeric columns found for standardization.")
