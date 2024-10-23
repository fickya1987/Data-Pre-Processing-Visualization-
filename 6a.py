import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
from scipy.stats import chi2_contingency

# Set page configuration
st.set_page_config(page_title="📊 6a.py - Advanced Data Preprocessing App", 
                   page_icon="📊", layout="wide")

# Function to handle missing values
def handle_missing_values(data):
    data = data.copy()
    for col in data.columns:
        if data[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(data[col]):
                data[col].fillna(data[col].mean(), inplace=True)
            else:
                data[col].fillna(data[col].mode()[0], inplace=True)
    return data

# Function for moving average smoothing
def custom_moving_average(data, window_size):
    smoothed_data = data.copy()
    for col in data.select_dtypes(include=np.number).columns:
        smoothed_data[col] = data[col].rolling(window=window_size, min_periods=1).mean()
    return smoothed_data

# Function for Min-Max Normalization with user input
def custom_min_max_normalization(data, min_value, max_value):
    normalized_data = data.copy()
    for col in data.select_dtypes(include=np.number).columns:
        col_min, col_max = data[col].min(), data[col].max()
        if col_min != col_max:
            normalized_data[col] = (data[col] - min_value) / (max_value - min_value)
    return normalized_data

# Function for Pearson Correlation Matrix
def custom_pearson_correlation(data):
    numeric_data = data.select_dtypes(include=np.number)
    corr_matrix = numeric_data.corr()
    return corr_matrix

# Function for Chi-Square Test
def custom_chi_square_test(data, col1, col2):
    contingency_table = pd.crosstab(data[col1], data[col2])
    chi2, p = chi2_contingency(contingency_table)[:2]
    return chi2, p, contingency_table

# Function for Boundary-Based Binning
def boundary_binning(data, col, boundaries):
    if pd.api.types.is_numeric_dtype(data[col]):
        # Use provided boundaries for binning
        data[f'{col}_binned'] = pd.cut(data[col], bins=boundaries, labels=False, include_lowest=True)
    else:
        st.error(f"Column '{col}' must be numeric for binning.")
        data[f'{col}_binned'] = np.nan
    return data

# Streamlit UI elements
st.title("📊 Advanced Data Preprocessing App")
st.write("Created by Prem Joshi")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview", df.head())

    # Handle missing values
    df = handle_missing_values(df)
    st.success("✅ Missing values handled successfully.")

    # Data Smoothing
    window_size = st.slider("Select window size for moving average", 1, 10, 3)
    smoothed_df = custom_moving_average(df, window_size)
    st.write("#### Smoothed Data (First 5 Rows)", smoothed_df.head())

    # Visualization for Smoothed Data
    st.write("### Smoothed Data Visualization")
    if st.checkbox("Show Smoothed Data Lines"):
        for col in smoothed_df.select_dtypes(include=np.number).columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=smoothed_df.index, y=smoothed_df[col], mode='lines', name='Smoothed'))
            fig.update_layout(title=f'Smoothed Data for {col}', xaxis_title='Index', yaxis_title='Value')
            st.plotly_chart(fig)

    # User Inputs for Min-Max Normalization
    min_value = st.number_input("Enter Min Value for Normalization", value=0.0)
    max_value = st.number_input("Enter Max Value for Normalization", value=1.0)
    normalized_df = custom_min_max_normalization(df, min_value, max_value)
    st.write("#### Normalized Data (First 5 Rows)", normalized_df.head())

    # Visualization for Normalized Data
    st.write("### Normalized Data Visualization")
    if st.checkbox("Show Normalized Data Lines"):
        for col in normalized_df.select_dtypes(include=np.number).columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=normalized_df.index, y=normalized_df[col], mode='lines', name='Normalized'))
            fig.update_layout(title=f'Normalized Data for {col}', xaxis_title='Index', yaxis_title='Normalized Value')
            st.plotly_chart(fig)

    # Pearson Correlation
    corr_matrix = custom_pearson_correlation(df)
    st.write("#### Pearson Correlation Matrix")
    st.dataframe(corr_matrix)

    # Pearson Correlation Heatmap
    st.write("### Pearson Correlation Heatmap")
    if st.checkbox("Show Heatmap"):
        fig = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='Viridis')
        st.plotly_chart(fig)

    # Chi-Square Test
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    col1 = st.selectbox("Select First Categorical Column", categorical_cols)
    col2 = st.selectbox("Select Second Categorical Column", categorical_cols)

    if st.button("Run Chi-Square Test"):
        chi2, p, contingency_table = custom_chi_square_test(df, col1, col2)
        st.write(f"Chi-Square Statistic: {chi2:.4f}, p-value: {p:.4f}")
        st.dataframe(contingency_table)

    # Boundary-Based Binning
    st.write("### Boundary-Based Binning")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    bin_col = st.selectbox("Select Column for Binning", numeric_cols)
    boundaries = st.text_input("Enter boundaries separated by commas (e.g., 0,10,20,30)")
    if boundaries:
        boundary_list = [float(x) for x in boundaries.split(',')]
        binned_df = boundary_binning(df, bin_col, boundary_list)
        st.write("#### Binned Data (First 5 Rows)", binned_df[[bin_col, f'{bin_col}_binned']].head())

        # Visualization for Binned Data
        if st.checkbox("Show Binned Data Distribution"):
            fig = go.Figure()
            fig.add_trace(go.Bar(x=binned_df[f'{bin_col}_binned'].value_counts().index,
                                  y=binned_df[f'{bin_col}_binned'].value_counts().values))
            fig.update_layout(title=f'Binned Data Distribution for {bin_col}', xaxis_title='Bins', yaxis_title='Frequency')
            st.plotly_chart(fig)
