import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from src.data_loader import fetch_market_data, fetch_fundamentals
from src.optimization_engine import (
    calculate_portfolio_performance, 
    calculate_unsystematic_risk, 
    get_efficient_frontier,
    rank_candidates_by_risk_reduction,
<<<<<<< HEAD
    ensure_metrics_json,
    METRICS_FILE
=======
    ensure_metrics_json
>>>>>>> 248f8fec53b4d47b47c5453e7a885e87a51fdf58
)

st.set_page_config(page_title="Portfolio AI", layout="wide")

with st.spinner("Initializing Data Engine..."):
    ensure_metrics_json()

try:
<<<<<<< HEAD
    with open(METRICS_FILE, "r") as f:
=======
    with open("assets_metrics.json", "r") as f:
>>>>>>> 248f8fec53b4d47b47c5453e7a885e87a51fdf58
        ASSET_METRICS = pd.DataFrame(json.load(f))
    if ASSET_METRICS.empty:
        st.error("Metrics file is empty. Please delete it and restart app.")
        st.stop()
except:
    st.error("Failed to load metrics. Please refresh.")
    st.stop()

if 'portfolio' not in st.session_state: st.session_state.portfolio = []

# --- SIDEBAR ---
st.sidebar.header("1. Build Portfolio")
lookback = st.sidebar.selectbox("Analysis Period", ["1 Year", "3 Years", "5 Years"], index=0)
start_date_map = {"1 Year": "2024-01-01", "3 Years": "2022-01-01", "5 Years": "2020-01-01"}
START_DATE = start_date_map[lookback]

all_tickers = ASSET_METRICS["Ticker"].tolist()
sel_ticker = st.sidebar.selectbox("Add Stock", options=all_tickers)
qty = st.sidebar.number_input("Quantity", min_value=1, value=10)

if st.sidebar.button("Add Asset"):
    exists = next((i for i in st.session_state.portfolio if i["Ticker"] == sel_ticker), None)
    if exists: exists["Quantity"] += qty
    else: st.session_state.portfolio.append({"Ticker": sel_ticker, "Quantity": qty})

if st.sidebar.button("Reset Portfolio"): st.session_state.portfolio = []

# --- MAIN DASHBOARD ---
st.title("🛡️ Portfolio Analytics & Efficient Frontier")

<<<<<<< HEAD
# --- FIX START: ROBUST EMPTY CHECK ---
if not st.session_state.portfolio:
    st.info("👈 Please add stocks from the sidebar to begin.")
    st.stop()  # STOPS EXECUTION HERE if empty

port_df = pd.DataFrame(st.session_state.portfolio)

# Double check if DataFrame structure is valid
if port_df.empty or "Ticker" not in port_df.columns:
    st.info("👈 Please add stocks from the sidebar to begin.")
    st.stop() # STOPS EXECUTION HERE if dataframe is malformed
# --- FIX END ---

=======
# FIX: Check if portfolio is empty BEFORE accessing Ticker column
if not st.session_state.portfolio:
    st.info("👈 Please add stocks from the sidebar to begin.")
    st.stop()

port_df = pd.DataFrame(st.session_state.portfolio)
>>>>>>> 248f8fec53b4d47b47c5453e7a885e87a51fdf58
user_tickers = port_df["Ticker"].tolist()

with st.spinner("Fetching Real-time Data..."):
    data = fetch_market_data(user_tickers, start_date=START_DATE)
    
    if data.empty:
        st.error("Could not fetch data for selected tickers. Check internet or try different stocks.")
        st.stop()
        
    latest_prices = data.iloc[-1]
    
    # Calculate weights safely
    port_df["Current Price"] = port_df["Ticker"].map(latest_prices)
    port_df = port_df.dropna(subset=["Current Price"]) # Drop tickers that failed to fetch
    
    if port_df.empty:
        st.error("All selected tickers failed to download.")
        st.stop()

    port_df["Total Value"] = port_df["Quantity"] * port_df["Current Price"]
    total_val = port_df["Total Value"].sum()
    port_df["Weight"] = port_df["Total Value"] / total_val
    
    weights = port_df.set_index("Ticker")["Weight"].reindex(data.columns).fillna(0).values
    
    # FIX: fill_method=None
    returns = data.pct_change(fill_method=None).dropna()
    p_ret, p_vol = calculate_portfolio_performance(weights, returns)
    risk_breakdown = calculate_unsystematic_risk(weights, returns)

<<<<<<< HEAD

=======
>>>>>>> 248f8fec53b4d47b47c5453e7a885e87a51fdf58
# 2. PORTFOLIO VALUE CHART
st.subheader(f"💰 Portfolio Value (Current: ₹{total_val:,.0f})")
qty_series = port_df.set_index("Ticker")["Quantity"]
hist_val = data.mul(qty_series, axis=1).sum(axis=1)
st.plotly_chart(px.line(hist_val, labels={"value": "Portfolio Value (₹)"}), use_container_width=True)

<<<<<<< HEAD

=======
>>>>>>> 248f8fec53b4d47b47c5453e7a885e87a51fdf58
# 3. RISK METRICS & FRONTIER
c1, c2 = st.columns([1, 2])

with c1:
    st.subheader("Risk Breakdown")
    st.metric("Total Risk", f"{risk_breakdown['Total Risk']:.1%}")
    st.metric("Systematic (Market)", f"{risk_breakdown['Systematic Risk']:.1%}", help="Cannot be diversified.")
    st.metric("Unsystematic (You)", f"{risk_breakdown['Unsystematic Risk']:.1%}", help="Can be reduced by diversification!", delta_color="inverse")
    st.metric("Portfolio Beta", f"{risk_breakdown['Beta']:.2f}")

with c2:
    st.subheader("📍 Efficient Frontier")
    top_liquid = ASSET_METRICS.sort_values("Sharpe", ascending=False).head(15)["Ticker"].tolist()
    frontier_data = fetch_market_data(top_liquid, start_date=START_DATE).pct_change(fill_method=None).dropna()
    ef_df = get_efficient_frontier(frontier_data, num_portfolios=300)
    
    fig = px.scatter(ef_df, x="Risk", y="Return", color="Sharpe", title="Efficient Frontier Simulation", color_continuous_scale="Viridis")
    fig.add_trace(go.Scatter(x=[p_vol], y=[p_ret], mode='markers+text', marker=dict(color='red', size=15, symbol='star'), name='You', text=['YOU'], textposition="top center"))
    st.plotly_chart(fig, use_container_width=True)

<<<<<<< HEAD

=======
>>>>>>> 248f8fec53b4d47b47c5453e7a885e87a51fdf58
# 4. RECOMMENDATIONS
st.divider()
st.subheader("🚀 Smart Recommendations")
target_ret = st.slider("Target Return Expectation", 0.1, 0.5, 0.2)

if st.button("Find Best Additions"):
    with st.spinner("Analyzing 300+ Assets..."):
        candidates = ASSET_METRICS[ASSET_METRICS["Return"] >= target_ret].head(20)["Ticker"].tolist()
        cand_data = fetch_market_data(candidates, start_date=START_DATE)
        recs = rank_candidates_by_risk_reduction(returns, candidates, cand_data)
        top_5 = recs.head(5).copy()
        funds = fetch_fundamentals(top_5["Ticker"].tolist())
        final = top_5.merge(funds, on="Ticker", how="left")
        st.dataframe(final.style.format({
            "Risk Reduction": "{:.4f}",
            "P/E Ratio": "{:.1f}",
            "Div Yield": "{:.2f}%"
        }).background_gradient(subset=["Risk Reduction"], cmap="Greens"), use_container_width=True)
