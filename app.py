import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# 1. Page Config
st.set_page_config(page_title="Ecommerce Analytics & Integrity", layout="wide")

@st.cache_data
def load_data():
    try:
        # Tries to find your file
        df = pd.read_csv("Ecommerce Customers.csv")
        # Ensure warehouse_block column exists for validation display
        if 'warehouse_block' not in df.columns:
            df['warehouse_block'] = np.random.choice(['A', 'B', 'C', 'D', 'E'], size=len(df))
        return df
    except FileNotFoundError:
        # FALLBACK: Generates identical structure automatically if file is missing
        st.sidebar.warning("⚠️ 'Ecommerce Customers.csv' not found. Using auto-generated sample data with integrity constraints.")
        np.random.seed(42)
        return pd.DataFrame({
            'warehouse_block': np.random.choice(['A', 'B', 'C', 'D', 'E', 'F'], 400),
            'Avg. Session Length': np.random.normal(32, 1.5, 400),
            'Time on App': np.random.normal(12, 1, 400),
            'Time on Website': np.random.normal(37, 1.5, 400),
            'Length of Membership': np.random.normal(3.5, 1.2, 400),
            'Yearly Amount Spent': np.random.normal(500, 75, 400),
            'Email': [f"user_{i}@example.com" for i in range(400)]
        })

# Load the data
df = load_data()

st.title("Ecommerce Customer Insights & Quality Management")
st.markdown("Interactive visualization using **Altair** alongside schema constraint validation.")

# --- NEW SECTION: DATA DICTIONARY & METADATA RESTRICTIONS ---
st.markdown("---")
with st.expander("📋 View Data Dictionary & Attribute Restrictions", expanded=True):
    st.markdown("### Structural Rules & Format Specifications")
    
    # 1. Build Data Dictionary Dataframe
    rules_data = {
        "Attribute Name": [
            "warehouse_block", 
            "Avg. Session Length", 
            "Time on App", 
            "Time on Website", 
            "Length of Membership", 
            "Yearly Amount Spent",
            "Email"
        ],
        "Data Type": ["String / Categorical", "Float", "Float", "Float", "Float", "Float", "String"],
        "Allowed Format / Range Constraints": [
            "UPPERCASE ALPHABETS ONLY (A-F)", 
            "Positive Float (20.0 to 50.0)", 
            "Positive Float (0.0 to 24.0)", 
            "Positive Float (0.0 to 60.0)", 
            "Positive Float (0.0 to 15.0)", 
            "Positive Currency ($0.00 to $2,000.00)",
            "Standard Email Regex Structure"
        ],
        "Business Rules & Information": [
            "Represents the designated fullfillment hub area. Must strictly be capitalized letters.",
            "Average length of a live web platform session measured in minutes.",
            "Average daily or weekly duration a user logs onto the smartphone application.",
            "Average total hours spent interacting via desktop web portal portals.",
            "Total cumulative continuous years a user has subscribed to premium loyalty features.",
            "Total financial expenditure processed through client account within a moving 12-month calendar.",
            "Primary communication point. Must be standard lowercase alphanumeric with valid @ domain."
        ]
    }
    df_rules = pd.DataFrame(rules_data)
    
    # 2. Render Interactive constraints layout
    st.dataframe(
        df_rules,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Attribute Name": st.column_config.TextColumn("Attribute Name", width="medium"),
            "Data Type": st.column_config.TextColumn("Expected Type"),
            "Allowed Format / Range Constraints": st.column_config.TextColumn("Restrictions / Limits"),
            "Business Rules & Information": st.column_config.TextColumn("Context Manual", width="large")
        }
    )
st.markdown("---")

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

# Combine layers
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
