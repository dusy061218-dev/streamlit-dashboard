import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# 1. Page Config
st.set_page_config(page_title="Ecommerce Analytics", layout="wide")

@st.cache_data
def load_data():
    try:
        # Tries to find your file
        return pd.read_csv("Ecommerce Customers.csv")
    except FileNotFoundError:
        # FALLBACK: Generates identical structure automatically if file is missing
        st.sidebar.warning("⚠️ 'Ecommerce Customers.csv' not found. Using auto-generated sample data instead.")
        np.random.seed(42)
        return pd.DataFrame({
            'Avg. Session Length': np.random.normal(32, 1.5, 400),
            'Time on App': np.random.normal(12, 1, 400),
            'Time on Website': np.random.normal(37, 1.5, 400),
            'Length of Membership': np.random.normal(3.5, 1.2, 400),
            'Yearly Amount Spent': np.random.normal(500, 75, 400),
            'Email': [f"user_{i}@example.com" for i in range(400)]
        })

# Load the data
df = load_data()

st.title("Ecommerce Customer Insights")
st.markdown("Interactive visualization using **Altair**.")

# 2. Sidebar Selection
features = ["Avg. Session Length", "Time on App", "Time on Website", "Length of Membership"]
selected_feature = st.sidebar.selectbox("Select Feature to Compare vs Spend:", features)

# --- CHART 1: Scatter Plot with Regression Line ---
st.subheader(f"Correlation: {selected_feature} vs. Spending")

# Base layer configuration
chart_base = alt.Chart(df).encode(
    x=alt.X(f'{selected_feature}:Q', title=selected_feature, scale=alt.Scale(zero=False)),
    y=alt.Y('Yearly Amount Spent:Q', title='Yearly Amount Spent ($)')
)

# Individual data points layer
scatter = chart_base.mark_circle(size=60, opacity=0.5, color="#1f77b4").encode(
    tooltip=['Email', 'Length of Membership', 'Yearly Amount Spent']
)

# Linear regression layer
regression = chart_base.transform_regression(
    selected_feature, 'Yearly Amount Spent'
).mark_line(color='red', size=3)

# Combine layers (Removed legacy width='container' parameters which cause errors)
combined_chart = (scatter + regression).properties(
    height=450
).interactive()

st.altair_chart(combined_chart, use_container_width=True)


# --- CHART 2: Distribution of Spending (Histogram) ---
st.subheader("Distribution of Yearly Amount Spent")

hist = alt.Chart(df).mark_bar().encode(
    x=alt.X("Yearly Amount Spent:Q", bin=alt.Bin(maxbins=30), title="Yearly Amount Spent ($)"),
    y=alt.Y('count()', title="Number of Customers"),
    color=alt.value("#4c78a8")
).properties(
    height=300
)

st.altair_chart(hist, use_container_width=True)

# 3. Data Inspection table
with st.expander("🔍 Preview Raw Dataset"):
    st.dataframe(df, use_container_width=True)
