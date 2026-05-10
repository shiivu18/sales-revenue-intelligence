# ============================================================
# SALES & REVENUE INTELLIGENCE PLATFORM
# STREAMLIT DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sales Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

customers = pd.read_csv(
    r"C:\Users\shokd\Desktop\Superstore\sales-revenue-intelligence\data\processed\customer_segments.csv"
)

monthly = pd.read_csv(
    r"C:\Users\shokd\Desktop\Superstore\sales-revenue-intelligence\data\processed\monthly_revenue.csv"
)

monthly['date'] = pd.to_datetime(
    monthly['date']
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Filters")

segment_filter = st.sidebar.multiselect(
    "Customer Segment",
    options=customers['segment_name'].unique(),
    default=customers['segment_name'].unique()
)

customers_filtered = customers[
    customers['segment_name'].isin(segment_filter)
]

# ============================================================
# TITLE
# ============================================================

st.title("📊 Sales & Revenue Intelligence Platform")

st.markdown("""
End-to-end analytics platform with:
- Churn prediction
- Customer segmentation
- Revenue forecasting
- Business intelligence KPIs
""")

# ============================================================
# KPI ROW
# ============================================================

total_customers = len(customers_filtered)

total_revenue = customers_filtered['monetary'].sum()

avg_revenue = customers_filtered['monetary'].mean()

high_risk = (
    customers_filtered['churn_risk']
    .eq('High risk')
    .sum()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Customers",
    f"{total_customers:,}"
)

c2.metric(
    "Revenue",
    f"${total_revenue:,.0f}"
)

c3.metric(
    "Avg Customer Value",
    f"${avg_revenue:,.0f}"
)

c4.metric(
    "High Risk Customers",
    f"{high_risk:,}"
)

# ============================================================
# CHURN DISTRIBUTION
# ============================================================

st.subheader("Customer Churn Risk")

risk_counts = (
    customers_filtered['churn_risk']
    .value_counts()
    .reset_index()
)

fig_risk = px.pie(
    risk_counts,
    names='churn_risk',
    values='count',
    hole=0.4
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)

# ============================================================
# CUSTOMER SEGMENTS
# ============================================================

st.subheader("Customer Segments")

fig_seg = px.scatter(
    customers_filtered,
    x='recency',
    y='monetary',
    size='frequency',
    color='segment_name',
    hover_data=['customer_id'],
    title='RFM Customer Segments'
)

st.plotly_chart(
    fig_seg,
    use_container_width=True
)

# ============================================================
# REVENUE TREND
# ============================================================

st.subheader("Revenue Forecast")

fig_rev = go.Figure()

fig_rev.add_trace(

    go.Scatter(
        x=monthly['date'],
        y=monthly['revenue'],
        mode='lines+markers',
        name='Revenue'
    )

)

st.plotly_chart(
    fig_rev,
    use_container_width=True
)

# ============================================================
# TOP CUSTOMERS
# ============================================================

st.subheader("Top Customers")

top_customers = (
    customers_filtered
    .sort_values(
        'monetary',
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_customers[
        [
            'customer_id',
            'monetary',
            'frequency',
            'segment_name',
            'churn_risk'
        ]
    ]
)

# ============================================================
# DOWNLOADS
# ============================================================

st.subheader("Download Data")

csv = customers_filtered.to_csv(index=False)

st.download_button(
    label="Download Customer Data",
    data=csv,
    file_name="customer_segments.csv",
    mime="text/csv"
)