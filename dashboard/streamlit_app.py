# ============================================================
# Sales & Revenue Intelligence Platform
# Phase 4 — Streamlit Dashboard
# ============================================================

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sales Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# STYLING
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    #MainMenu {visibility: hidden;}
    footer     {visibility: hidden;}
    header     {visibility: hidden;}

    .stApp {
        background-color: #0f1117;
        color: #e8eaf0;
    }

    section[data-testid="stSidebar"] {
        background-color: #161b27;
        border-right: 1px solid #252d3d;
    }

    .kpi-card {
        background: linear-gradient(135deg, #1a2035 0%, #1e2840 100%);
        border: 1px solid #2a3550;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 4px;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #6b7a99;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'DM Mono', monospace;
        font-size: 28px;
        font-weight: 500;
        color: #e8eaf0;
        line-height: 1.1;
    }
    .kpi-delta-pos { font-size: 12px; color: #34d399; margin-top: 4px; }
    .kpi-delta-neg { font-size: 12px; color: #f87171; margin-top: 4px; }
    .kpi-delta-neu { font-size: 12px; color: #6b7a99; margin-top: 4px; }

    .section-header {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #4f6ef7;
        border-bottom: 1px solid #252d3d;
        padding-bottom: 8px;
        margin: 24px 0 16px 0;
    }

    .page-title {
        font-size: 22px;
        font-weight: 700;
        color: #e8eaf0;
        margin-bottom: 2px;
    }
    .page-subtitle {
        font-size: 13px;
        color: #6b7a99;
        margin-bottom: 24px;
    }

    .badge-high   { background:#2d1515; color:#f87171; border:1px solid #7f1d1d; border-radius:6px; padding:2px 10px; font-size:11px; font-weight:600; }
    .badge-medium { background:#2d2515; color:#fbbf24; border:1px solid #78350f; border-radius:6px; padding:2px 10px; font-size:11px; font-weight:600; }
    .badge-low    { background:#152d1e; color:#34d399; border:1px solid #064e3b; border-radius:6px; padding:2px 10px; font-size:11px; font-weight:600; }

    .stDataFrame { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PATHS
# ============================================================

BASE_DIR   = Path(__file__).resolve().parent.parent
DB_PATH    = BASE_DIR / "data" / "processed" / "superstore.db"
SEG_PATH   = BASE_DIR / "data" / "processed" / "customer_segments.csv"
MONTH_PATH = BASE_DIR / "data" / "processed" / "monthly_revenue.csv"

# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_orders() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM orders", conn)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


@st.cache_data
def load_segments() -> pd.DataFrame:
    df = pd.read_csv(SEG_PATH)
    df["first_order"] = pd.to_datetime(df["first_order"])
    df["last_order"]  = pd.to_datetime(df["last_order"])
    return df


@st.cache_data
def load_monthly() -> pd.DataFrame:
    df = pd.read_csv(MONTH_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df


orders  = load_orders()
segs    = load_segments()
monthly = load_monthly()

# ============================================================
# PLOTLY THEME
# ============================================================

CHART_THEME = dict(
    plot_bgcolor  = "#161b27",
    paper_bgcolor = "#161b27",
    font          = dict(family="DM Sans", color="#9aa3b8", size=12),
    xaxis         = dict(gridcolor="#252d3d", linecolor="#252d3d", tickfont=dict(color="#6b7a99")),
    yaxis         = dict(gridcolor="#252d3d", linecolor="#252d3d", tickfont=dict(color="#6b7a99")),
    legend        = dict(bgcolor="#1a2035", bordercolor="#252d3d", borderwidth=1),
    margin        = dict(l=16, r=16, t=36, b=16),
)

SEG_COLORS = {
    "Champions":       "#34d399",
    "Loyal Customers": "#60a5fa",
    "High Value":      "#a78bfa",
    "Lost":            "#f87171",
}

# ============================================================
# SIDEBAR
# ============================================================

# FIX 1: Define page options as a constant so we can reference
#         them consistently in both the radio and the if/elif blocks
PAGES = [
    "🏠 Home",
    "📈 Executive Overview",
    "👥 Customer Intelligence",
    "⚠️ Churn Prediction",
    "🔮 Revenue Forecast",
]

with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 24px 0;'>
        <div style='font-size:18px;font-weight:700;color:#e8eaf0;'>📊 Sales Intel</div>
        <div style='font-size:11px;color:#4f6ef7;letter-spacing:1px;margin-top:2px;'>
            REVENUE INTELLIGENCE PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    # FIX 2: Indentation was broken in original — radio must be inside the `with` block
    page = st.radio(
        "Navigate",
        PAGES,
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#252d3d;margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:11px;color:#6b7a99;letter-spacing:1px;"
        "font-weight:600;margin-bottom:10px;'>GLOBAL FILTERS</div>",
        unsafe_allow_html=True,
    )

    all_years = sorted(orders["order_year"].unique())
    sel_years = st.multiselect("Year", all_years, default=all_years)

    all_regions = sorted(orders["region"].unique())
    sel_regions = st.multiselect("Region", all_regions, default=all_regions)

    all_segments = sorted(orders["segment"].unique())
    sel_segments = st.multiselect("Segment", all_segments, default=all_segments)

    st.markdown("<hr style='border-color:#252d3d;margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:10px;color:#3d4a63;line-height:1.6;'>
        Dataset: Superstore 2015–2018<br>
        Records: {len(orders):,} order lines<br>
        Customers: {orders['customer_id'].nunique():,}
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# GLOBAL FILTER — applied to orders for pages that need it
# ============================================================

# FIX 3: Guard against empty multiselect lists so the mask
#         doesn't silently drop all rows
if not sel_years:
    sel_years = all_years
if not sel_regions:
    sel_regions = all_regions
if not sel_segments:
    sel_segments = all_segments

mask = (
    orders["order_year"].isin(sel_years) &
    orders["region"].isin(sel_regions) &
    orders["segment"].isin(sel_segments)
)
df = orders[mask].copy()

# ============================================================
# HELPER: KPI card
# ============================================================

def kpi(label: str, value: str, delta: str = "", delta_type: str = "neu"):
    delta_class = f"kpi-delta-{delta_type}"
    delta_html  = f'<div class="{delta_class}">{delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FIX 4: All page blocks use `if page == PAGES[n]` with the
#         EXACT same string defined in PAGES — no more mismatches.
#         Also changed all `elif` after Home to `if` so each page
#         is independent (elif chains break when page order shifts).
# ============================================================

# ============================================================
# PAGE 0 — HOME
# ============================================================

if page == "🏠 Home":
    st.markdown("""
    <div style='padding: 60px 0 40px 0; text-align: center;'>
        <div style='font-size: 48px; margin-bottom: 16px;'>📊</div>
        <div style='font-size: 32px; font-weight: 700; color: #e8eaf0; margin-bottom: 8px;'>
            Sales &amp; Revenue Intelligence Platform
        </div>
        <div style='font-size: 16px; color: #6b7a99; margin-bottom: 48px;'>
            Built on Superstore 2015–2018 · Python · SQL · Machine Learning · Streamlit
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="kpi-card" style='margin-bottom:16px;'>
            <div style='font-size:20px; margin-bottom:8px;'>📈</div>
            <div style='font-size:15px; font-weight:600; color:#e8eaf0; margin-bottom:4px;'>Executive Overview</div>
            <div style='font-size:12px; color:#6b7a99;'>Revenue trends, YoY growth, regional and category performance KPIs</div>
        </div>
        <div class="kpi-card">
            <div style='font-size:20px; margin-bottom:8px;'>⚠️</div>
            <div style='font-size:15px; font-weight:600; color:#e8eaf0; margin-bottom:4px;'>Churn Prediction</div>
            <div style='font-size:12px; color:#6b7a99;'>Random Forest model · ROC-AUC 0.814 · Actionable at-risk customer list</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="kpi-card" style='margin-bottom:16px;'>
            <div style='font-size:20px; margin-bottom:8px;'>👥</div>
            <div style='font-size:15px; font-weight:600; color:#e8eaf0; margin-bottom:4px;'>Customer Intelligence</div>
            <div style='font-size:12px; color:#6b7a99;'>RFM segmentation · K-Means clustering · Champions, Loyal, High Value, Lost</div>
        </div>
        <div class="kpi-card">
            <div style='font-size:20px; margin-bottom:8px;'>🔮</div>
            <div style='font-size:15px; font-weight:600; color:#e8eaf0; margin-bottom:4px;'>Revenue Forecast</div>
            <div style='font-size:12px; color:#6b7a99;'>Linear Regression · Lag features · Seasonality · MoM growth analysis</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        "<div class='section-header' style='margin-top:40px;'>Platform at a glance</div>",
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: kpi("Order Lines",  f"{len(orders):,}",               "2015–2018")
    with m2: kpi("Customers",    f"{orders['customer_id'].nunique():,}", "unique buyers")
    with m3: kpi("ML Models",    "3",                               "RF · KMeans · LR")
    with m4: kpi("ROC-AUC",      "0.814",                           "churn model", "pos")
    with m5: kpi("Churn Rate",   "25.9%",                           "180-day threshold", "neg")

    st.markdown("""
    <div style='margin-top:40px; padding:16px 20px; background:#1a2035;
                border-radius:8px; border-left:3px solid #4f6ef7;
                font-size:12px; color:#6b7a99; line-height:1.8;'>
        <strong style='color:#4f6ef7;'>Tech stack:</strong>
        Python · Pandas · NumPy · Scikit-learn · SQLite · SQL · Streamlit · Plotly ·
        Random Forest · K-Means · Linear Regression · RFM Analysis · Cohort Analysis
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ============================================================

if page == "📈 Executive Overview":

    st.markdown('<div class="page-title">Executive Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Top-line revenue performance across all regions and segments</div>',
        unsafe_allow_html=True,
    )

    # ── KPI row ──────────────────────────────────────────────
    total_rev    = df["sales"].sum()
    total_orders = df["order_id"].nunique()
    total_custs  = df["customer_id"].nunique()
    aov          = total_rev / total_orders if total_orders else 0

    yoy_text = ""
    yoy_type = "neu"
    if len(sel_years) >= 2:
        latest     = sorted(sel_years)[-1]
        prior      = sorted(sel_years)[-2]
        rev_latest = df[df["order_year"] == latest]["sales"].sum()
        rev_prior  = df[df["order_year"] == prior]["sales"].sum()
        if rev_prior > 0:
            growth   = (rev_latest - rev_prior) / rev_prior * 100
            yoy_text = f"{'▲' if growth >= 0 else '▼'} {abs(growth):.1f}% vs {prior}"
            yoy_type = "pos" if growth >= 0 else "neg"

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi("Total Revenue",    f"${total_rev:,.0f}",  yoy_text, yoy_type)
    with k2: kpi("Total Orders",     f"{total_orders:,}",   f"{total_orders / max(len(sel_years), 1):,.0f} avg/year")
    with k3: kpi("Active Customers", f"{total_custs:,}",    "unique buyers")
    with k4: kpi("Avg Order Value",  f"${aov:,.0f}",        "per order")

    # ── Revenue trend ─────────────────────────────────────────
    st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)

    # FIX 5: Use dt.to_period safely then convert back
    monthly_filt = (
        df.groupby(df["order_date"].dt.to_period("M"))["sales"]
        .sum()
        .reset_index()
    )
    monthly_filt.columns = ["period", "sales"]
    monthly_filt["order_date"] = monthly_filt["period"].dt.to_timestamp()
    monthly_filt["rolling3"]   = monthly_filt["sales"].rolling(3, center=True).mean()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=monthly_filt["order_date"], y=monthly_filt["sales"],
        name="Monthly Revenue", marker_color="#2a3a6e", opacity=0.8,
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly_filt["order_date"], y=monthly_filt["rolling3"],
        name="3-Month Avg", line=dict(color="#4f6ef7", width=2.5),
        mode="lines",
    ))
    fig_trend.update_layout(
        **CHART_THEME,
        title="Monthly Revenue with 3-Month Rolling Average",
        yaxis_tickprefix="$", yaxis_tickformat=",.0f",
        height=320, hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # ── Category + Region ────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-header">Revenue by Category</div>', unsafe_allow_html=True)
        cat = (
            df.groupby("category")["sales"]
            .sum()
            .reset_index()
            .sort_values("sales", ascending=True)
        )
        fig_cat = px.bar(
            cat, x="sales", y="category", orientation="h",
            color="sales",
            color_continuous_scale=["#1a2035", "#4f6ef7"],
            labels={"sales": "Revenue ($)", "category": ""},
        )
        fig_cat.update_layout(**CHART_THEME, height=240, showlegend=False, coloraxis_showscale=False)
        fig_cat.update_traces(hovertemplate="$%{x:,.0f}")
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">Revenue by Region</div>', unsafe_allow_html=True)
        reg = df.groupby("region")["sales"].sum().reset_index()
        fig_reg = px.pie(
            reg, values="sales", names="region",
            color_discrete_sequence=["#4f6ef7", "#34d399", "#fbbf24", "#f87171"],
            hole=0.55,
        )
        fig_reg.update_layout(**CHART_THEME, height=240)
        fig_reg.update_traces(
            textinfo="percent+label",
            hovertemplate="%{label}: $%{value:,.0f}",
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    # ── YoY comparison table ──────────────────────────────────
    st.markdown('<div class="section-header">Year-over-Year Performance</div>', unsafe_allow_html=True)
    yoy = (
        df.groupby("order_year")
        .agg(
            Revenue   = ("sales",       "sum"),
            Orders    = ("order_id",    "nunique"),
            Customers = ("customer_id", "nunique"),
            Avg_Order = ("sales",       "mean"),
        )
        .reset_index()
        .rename(columns={"order_year": "Year"})
    )
    yoy["Revenue"]   = yoy["Revenue"].map("${:,.0f}".format)
    yoy["Avg_Order"] = yoy["Avg_Order"].map("${:,.0f}".format)
    st.dataframe(yoy, use_container_width=True, hide_index=True)


# ============================================================
# PAGE 2 — CUSTOMER INTELLIGENCE
# ============================================================

if page == "👥 Customer Intelligence":

    st.markdown('<div class="page-title">Customer Intelligence</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">RFM segmentation · lifetime value · customer behaviour analysis</div>',
        unsafe_allow_html=True,
    )

    # ── Segment KPIs ─────────────────────────────────────────
    seg_counts = segs["segment_name"].value_counts()
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi("Champions",       str(seg_counts.get("Champions", 0)),       "Low recency · High revenue", "pos")
    with k2: kpi("Loyal Customers", str(seg_counts.get("Loyal Customers", 0)), "Core customer base",         "pos")
    with k3: kpi("High Value",      str(seg_counts.get("High Value", 0)),       "Highest avg spend",          "neu")
    with k4: kpi("Lost",            str(seg_counts.get("Lost", 0)),             "556+ days inactive",         "neg")

    # ── RFM scatter ───────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Customer Map — Recency vs Lifetime Revenue</div>',
        unsafe_allow_html=True,
    )

    fig_rfm = px.scatter(
        segs,
        x="recency", y="monetary",
        size="frequency", color="segment_name",
        color_discrete_map=SEG_COLORS,
        hover_name="customer_id",
        hover_data={
            "recency":      True,
            "monetary":     ":.0f",
            "frequency":    True,
            "segment_name": True,
        },
        labels={
            "recency":      "Recency (days since last order)",
            "monetary":     "Lifetime Revenue ($)",
            "segment_name": "Segment",
        },
        size_max=30,
    )
    fig_rfm.update_layout(
        **CHART_THEME,
        height=420,
        title="Bubble size = purchase frequency",
    )
    st.plotly_chart(fig_rfm, use_container_width=True)

    # ── Segment revenue + avg metrics ─────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-header">Revenue Contribution by Segment</div>', unsafe_allow_html=True)
        seg_rev = (
            segs.groupby("segment_name")["monetary"]
            .sum()
            .reset_index()
            .sort_values("monetary")
        )
        fig_seg = px.bar(
            seg_rev, x="monetary", y="segment_name", orientation="h",
            color="segment_name", color_discrete_map=SEG_COLORS,
            labels={"monetary": "Total Revenue ($)", "segment_name": ""},
        )
        fig_seg.update_layout(**CHART_THEME, height=280, showlegend=False)
        fig_seg.update_traces(hovertemplate="$%{x:,.0f}")
        st.plotly_chart(fig_seg, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">Avg Revenue per Customer</div>', unsafe_allow_html=True)
        seg_avg = (
            segs.groupby("segment_name")["monetary"]
            .mean()
            .reset_index()
            .sort_values("monetary")
        )
        fig_avg = px.bar(
            seg_avg, x="monetary", y="segment_name", orientation="h",
            color="segment_name", color_discrete_map=SEG_COLORS,
            labels={"monetary": "Avg Revenue ($)", "segment_name": ""},
        )
        fig_avg.update_layout(**CHART_THEME, height=280, showlegend=False)
        fig_avg.update_traces(hovertemplate="$%{x:,.0f}")
        st.plotly_chart(fig_avg, use_container_width=True)

    # ── Top 20 customers table ────────────────────────────────
    st.markdown('<div class="section-header">Top 20 Customers by Lifetime Revenue</div>', unsafe_allow_html=True)

    seg_filter = st.selectbox("Filter by segment", ["All"] + sorted(segs["segment_name"].unique()))
    top_df = segs.copy()
    if seg_filter != "All":
        top_df = top_df[top_df["segment_name"] == seg_filter]

    top20 = (
        top_df
        .nlargest(20, "monetary")
        [["customer_id", "segment_name", "monetary", "frequency", "recency", "churn_risk"]]
        .rename(columns={
            "customer_id":  "Customer ID",
            "segment_name": "Segment",
            "monetary":     "Lifetime Revenue",
            "frequency":    "Orders",
            "recency":      "Days Since Last Order",
            "churn_risk":   "Churn Risk",
        })
    )
    top20["Lifetime Revenue"] = top20["Lifetime Revenue"].map("${:,.0f}".format)
    st.dataframe(top20, use_container_width=True, hide_index=True)


# ============================================================
# PAGE 3 — CHURN PREDICTION
# ============================================================

if page == "⚠️ Churn Prediction":

    st.markdown('<div class="page-title">Churn Prediction</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Random Forest · ROC-AUC 0.814 · 180-day churn threshold</div>',
        unsafe_allow_html=True,
    )

    # ── Risk KPIs ─────────────────────────────────────────────
    high        = (segs["churn_risk"] == "High risk").sum()
    medium      = (segs["churn_risk"] == "Medium risk").sum()
    low         = (segs["churn_risk"] == "Low risk").sum()
    at_risk_rev = segs[segs["churn_risk"] == "High risk"]["monetary"].sum()

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi("High Risk Customers", str(high),              "Immediate action needed", "neg")
    with k2: kpi("Medium Risk",         str(medium),            "Monitor closely",         "neu")
    with k3: kpi("Low Risk",            str(low),               "Healthy customers",       "pos")
    with k4: kpi("Revenue at Risk",     f"${at_risk_rev:,.0f}", "From high-risk customers","neg")

    # ── Churn probability distribution ────────────────────────
    st.markdown('<div class="section-header">Churn Probability Distribution</div>', unsafe_allow_html=True)

    fig_dist = px.histogram(
        segs, x="churn_probability",
        color="churn_risk",
        color_discrete_map={
            "High risk":   "#f87171",
            "Medium risk": "#fbbf24",
            "Low risk":    "#34d399",
        },
        nbins=40,
        labels={
            "churn_probability": "Predicted Churn Probability",
            "churn_risk":        "Risk Tier",
        },
        barmode="overlay",
        opacity=0.75,
    )
    fig_dist.add_vline(
        x=0.3, line_dash="dash", line_color="#6b7a99",
        annotation_text="Low/Medium boundary",
        annotation_font_color="#6b7a99",
    )
    fig_dist.add_vline(
        x=0.6, line_dash="dash", line_color="#fbbf24",
        annotation_text="Medium/High boundary",
        annotation_font_color="#fbbf24",
    )
    fig_dist.update_layout(**CHART_THEME, height=320)
    st.plotly_chart(fig_dist, use_container_width=True)

    # ── Risk by segment ───────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-header">Churn Risk by Customer Segment</div>', unsafe_allow_html=True)
        risk_seg = (
            segs.groupby(["segment_name", "churn_risk"])
            .size()
            .reset_index(name="count")
        )
        fig_rs = px.bar(
            risk_seg,
            x="segment_name", y="count", color="churn_risk",
            color_discrete_map={
                "High risk":   "#f87171",
                "Medium risk": "#fbbf24",
                "Low risk":    "#34d399",
            },
            labels={"segment_name": "", "count": "Customers", "churn_risk": "Risk"},
            barmode="stack",
        )
        fig_rs.update_layout(**CHART_THEME, height=320)
        st.plotly_chart(fig_rs, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">Avg Revenue by Risk Tier</div>', unsafe_allow_html=True)
        risk_rev = (
            segs.groupby("churn_risk")["monetary"]
            .mean()
            .reset_index()
        )
        fig_rr = px.bar(
            risk_rev,
            x="churn_risk", y="monetary",
            color="churn_risk",
            color_discrete_map={
                "High risk":   "#f87171",
                "Medium risk": "#fbbf24",
                "Low risk":    "#34d399",
            },
            labels={"churn_risk": "", "monetary": "Avg Lifetime Revenue ($)"},
        )
        fig_rr.update_layout(**CHART_THEME, height=320, showlegend=False)
        fig_rr.update_traces(hovertemplate="$%{y:,.0f}")
        st.plotly_chart(fig_rr, use_container_width=True)

    # ── Action list ───────────────────────────────────────────
    st.markdown('<div class="section-header">Customers Requiring Immediate Action</div>', unsafe_allow_html=True)
    st.caption("Sorted by lifetime revenue — prioritise outreach from highest value down")

    risk_filter = st.selectbox("Risk tier", ["High risk", "Medium risk", "Low risk"])

    action_df = (
        segs[segs["churn_risk"] == risk_filter]
        .sort_values("monetary", ascending=False)
        [["customer_id", "segment_name", "monetary", "frequency",
          "recency", "churn_probability", "region"]]
        .rename(columns={
            "customer_id":       "Customer ID",
            "segment_name":      "Segment",
            "monetary":          "Lifetime Revenue",
            "frequency":         "Total Orders",
            "recency":           "Days Inactive",
            "churn_probability": "Churn Probability",
            "region":            "Region",
        })
        .head(25)
    )
    action_df["Lifetime Revenue"]  = action_df["Lifetime Revenue"].map("${:,.0f}".format)
    action_df["Churn Probability"] = action_df["Churn Probability"].map("{:.1%}".format)
    st.dataframe(action_df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div style='font-size:12px;color:#4f6ef7;margin-top:12px;padding:12px 16px;
                background:#1a2035;border-radius:8px;border-left:3px solid #4f6ef7;'>
        💡 <strong>Recommended actions:</strong>
        High-risk customers with high lifetime revenue should receive personalised outreach within 7 days.
        Consider win-back campaigns with exclusive offers for Lost segment customers.
        Champions with rising churn probability may need an account review call.
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# PAGE 4 — REVENUE FORECAST
# ============================================================

if page == "🔮 Revenue Forecast":

    st.markdown('<div class="page-title">Revenue Forecast</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Linear Regression · 6-month holdout · lag + rolling features</div>',
        unsafe_allow_html=True,
    )

    # ── Forecast KPIs ─────────────────────────────────────────
    latest_month_rev = monthly["revenue"].iloc[-1]
    avg_rev          = monthly["revenue"].mean()
    peak_idx         = monthly["revenue"].idxmax()
    peak_month       = monthly.loc[peak_idx, "date"].strftime("%b %Y")
    peak_rev         = monthly["revenue"].max()
    total_months     = len(monthly)

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi("Latest Month Revenue", f"${latest_month_rev:,.0f}", monthly["date"].iloc[-1].strftime("%b %Y"))
    with k2: kpi("Monthly Average",      f"${avg_rev:,.0f}",          f"over {total_months} months")
    with k3: kpi("Peak Month",           peak_month,                   f"${peak_rev:,.0f}")
    with k4: kpi("Forecast Model",       "Lin. Reg.",                  "lag + rolling features", "pos")

    # ── Full revenue trend ────────────────────────────────────
    st.markdown(
        '<div class="section-header">Revenue Trend — Full History with Rolling Average</div>',
        unsafe_allow_html=True,
    )

    fig_full = go.Figure()
    fig_full.add_trace(go.Bar(
        x=monthly["date"], y=monthly["revenue"],
        name="Actual Revenue",
        marker_color="#2a3a6e", opacity=0.7,
    ))
    fig_full.add_trace(go.Scatter(
        x=monthly["date"], y=monthly["rolling3"],
        name="3-Month Rolling Avg",
        line=dict(color="#4f6ef7", width=2.5),
        mode="lines",
    ))
    fig_full.update_layout(
        **CHART_THEME,
        height=340,
        yaxis_tickprefix="$", yaxis_tickformat=",.0f",
        hovermode="x unified",
        title="Monthly Revenue 2015–2018",
    )
    st.plotly_chart(fig_full, use_container_width=True)

    # ── Seasonality analysis ──────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-header">Seasonality — Avg Revenue by Month</div>', unsafe_allow_html=True)

        # FIX 6: Derive month_of_year from the date column if not present
        if "month_of_year" not in monthly.columns:
            monthly["month_of_year"] = monthly["date"].dt.month

        season = (
            monthly.groupby("month_of_year")["revenue"]
            .mean()
            .reset_index()
        )
        month_names = {
            1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May",  6:"Jun",
            7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec",
        }
        season["month_name"] = season["month_of_year"].map(month_names)
        # Keep months in calendar order
        season = season.sort_values("month_of_year")

        fig_season = px.bar(
            season, x="month_name", y="revenue",
            color="revenue",
            color_continuous_scale=["#1a2035", "#4f6ef7", "#34d399"],
            labels={"month_name": "", "revenue": "Avg Revenue ($)"},
            category_orders={"month_name": list(month_names.values())},
        )
        fig_season.update_layout(**CHART_THEME, height=280, coloraxis_showscale=False)
        fig_season.update_traces(hovertemplate="%{x}: $%{y:,.0f}")
        st.plotly_chart(fig_season, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">Quarterly Revenue by Year</div>', unsafe_allow_html=True)

        orders_filt = orders[orders["order_year"].isin(sel_years)]
        qtr = (
            orders_filt
            .groupby(["order_year", "order_quarter"])["sales"]
            .sum()
            .reset_index()
        )
        qtr["label"] = "Q" + qtr["order_quarter"].astype(str)
        qtr["year"]  = qtr["order_year"].astype(str)

        fig_qtr = px.bar(
            qtr, x="label", y="sales", color="year",
            barmode="group",
            color_discrete_sequence=["#4f6ef7", "#34d399", "#fbbf24", "#f87171"],
            labels={"label": "Quarter", "sales": "Revenue ($)", "year": "Year"},
        )
        fig_qtr.update_layout(**CHART_THEME, height=280)
        fig_qtr.update_traces(hovertemplate="$%{y:,.0f}")
        st.plotly_chart(fig_qtr, use_container_width=True)

    # ── MoM growth table ──────────────────────────────────────
    st.markdown('<div class="section-header">Month-over-Month Revenue Detail</div>', unsafe_allow_html=True)

    mom = monthly.copy()
    mom["MoM_pct"] = mom["revenue"].pct_change() * 100

    mom_display = mom[["date", "revenue", "rolling3", "MoM_pct"]].copy()

    # FIX 7: Sort by actual datetime BEFORE formatting strings
    mom_display = mom_display.sort_values("date", ascending=False).head(24)

    mom_display["date"]    = mom_display["date"].dt.strftime("%b %Y")
    mom_display["revenue"] = mom_display["revenue"].map("${:,.0f}".format)
    mom_display["rolling3"] = mom_display["rolling3"].map(
        lambda x: f"${x:,.0f}" if pd.notna(x) else "—"
    )
    mom_display["MoM_pct"] = mom_display["MoM_pct"].map(
        lambda x: f"+{x:.1f}%" if pd.notna(x) and x >= 0 else (f"{x:.1f}%" if pd.notna(x) else "—")
    )
    mom_display.columns = ["Month", "Revenue", "3-Month Avg", "MoM Growth"]

    st.dataframe(mom_display, use_container_width=True, hide_index=True)