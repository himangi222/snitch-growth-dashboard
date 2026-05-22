import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Snitch Growth Dashboard",
    layout="wide"
)

# TITLE
st.title("Snitch Growth Intelligence Dashboard")

# DATABASE CONNECTION
conn = sqlite3.connect("data/snitch.db")

# SQL QUERY
query = """
SELECT
    category,
    COUNT(*) as visitors,
    SUM(viewed_pdp) as pdp_views,
    SUM(added_to_cart) as carts,
    SUM(purchased) as purchases
FROM funnel
GROUP BY category
"""

df = pd.read_sql(query, conn)

# CATEGORY FILTER
selected_category = st.selectbox(
    "Select Category",
    ["All"] + list(df['category'].unique())
)

# FILTER DATA
if selected_category != "All":
    filtered_df = df[df['category'] == selected_category]
else:
    filtered_df = df

# KPI CALCULATIONS
total_visitors = filtered_df['visitors'].sum()
total_purchases = filtered_df['purchases'].sum()
total_carts = filtered_df['carts'].sum()

conversion_rate = round(
    (total_purchases / total_visitors) * 100,
    2
)

cart_abandonment = round(
    ((total_carts - total_purchases) / total_carts) * 100,
    2
)

revenue = (filtered_df['purchases'] * 1500).sum()

# KPI CARDS
col1, col2, col3, col4 = st.columns(4)

col1.metric("Visitors", f"{total_visitors:,}")
col2.metric("Conversion Rate", f"{conversion_rate}%")
col3.metric("Cart Abandonment", f"{cart_abandonment}%")
col4.metric("Revenue", f"₹{revenue:,}")

# TABLE
st.subheader("Category Funnel Metrics")

st.dataframe(filtered_df)

# BAR CHART
fig = px.bar(
    filtered_df,
    x="category",
    y="purchases",
    title="Purchases by Category"
)

st.plotly_chart(fig)

# FUNNEL CHART
fig2 = px.funnel(
    x=[
        filtered_df['visitors'].sum(),
        filtered_df['pdp_views'].sum(),
        filtered_df['carts'].sum(),
        filtered_df['purchases'].sum()
    ],
    y=[
        "Visitors",
        "PDP Views",
        "Cart Adds",
        "Purchases"
    ]
)

st.plotly_chart(fig2)

# BUSINESS INSIGHTS
st.header("Key Business Insights")

st.markdown("""
- Shirts contribute highest purchases across catalog.
- Footwear shows lowest conversion contribution.
- Cart abandonment exceeds 60%, indicating recovery opportunity.
- Cargo and Jeans categories drive strong engagement.
- Stockouts may be reducing purchase completion in premium categories.
""")