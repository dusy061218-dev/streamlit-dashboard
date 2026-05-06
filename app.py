import streamlit as st
import pandas as pd
import altair as alt

# Page config
st.set_page_config(page_title="Ecommerce Analytics", layout="wide")

@st.cache_data
def load_data():
    # Referencing the file name verbatim
    return pd.read_csv("Ecommerce Customers.csv")

try:
    df = load_data()

    st.title("Ecommerce Customer Insights")
    st.markdown("Interactive visualization using **Altair**.")

    # Sidebar Selection
    features = ["Avg. Session Length", "Time on App", "Time on Website", "Length of Membership"]
    selected_feature = st.sidebar.selectbox("Select Feature to Compare vs Spend:", features)

    # 1. Scatter Plot with Regression Line
    chart_base = alt.Chart(df).encode(
        x=alt.X(f'{selected_feature}:Q', title=selected_feature),
        y=alt.Y('Yearly Amount Spent:Q', title='Yearly Amount Spent ($)')
    )

    scatter = chart_base.mark_circle(size=60, opacity=0.5, color="#1f77b4").encode(
        tooltip=['Email', 'Length of Membership', 'Yearly Amount Spent']
    )

    regression = chart_base.transform_regression(
        selected_feature, 'Yearly Amount Spent'
    ).mark_line(color='red', size=3)

    combined_chart = (scatter + regression).properties(
        width='container',
        height=500,
        title=f"Correlation: {selected_feature} vs. Spending"
    ).interactive()

    st.altair_chart(combined_chart, use_container_width=True)

    # 2. Distribution of Spending (Histogram)
    hist = alt.Chart(df).mark_bar().encode(
        x=alt.X("Yearly Amount Spent:Q", bin=alt.Bin(maxbins=30), title="Yearly Amount Spent"),
        y=alt.Y('count()', title="Number of Customers"),
        color=alt.value("#4c78a8")
    ).properties(
        width='container',
        height=300,
        title="Distribution of Yearly Amount Spent"
    )

    st.altair_chart(hist, use_container_width=True)

except FileNotFoundError:
    st.error("Please ensure 'Ecommerce Customers.csv' is in the same directory.")