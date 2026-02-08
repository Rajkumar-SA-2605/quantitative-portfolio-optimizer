import numpy as np
import pandas as pd
from scipy.optimize import minimize
import yfinance as yf
import json
import os
from src.constants import get_indian_tickers

TRADING_DAYS = 252
<<<<<<< HEAD
# Get the project root directory (2 levels up from src/optimization_engine.py)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS_FILE = os.path.join(PROJECT_ROOT, "assets_metrics.json")
=======
METRICS_FILE = "assets_metrics.json"
>>>>>>> 248f8fec53b4d47b47c5453e7a885e87a51fdf58

def ensure_metrics_json():
    if os.path.exists(METRICS_FILE):
        return
    
    print("⚠️ JSON file missing. Generating it now... (This happens only once)")
    tickers = get_indian_tickers()
    
    try:
        # Download 1 Year data
        data = yf.download(tickers, period="1y", auto_adjust=False, threads=True)['Adj Close']
        
        # Drop failed columns
        data = data.dropna(axis=1, how='all')
        
        # FIX: Explicitly set fill_method=None to silence warning
        returns = data.pct_change(fill_method=None)
        
        mean_ret = returns.mean() * TRADING_DAYS
        vol = returns.std() * np.sqrt(TRADING_DAYS)
        
        metrics = []
        rf = 0.06
        
        # Only include assets that actually have data
        valid_tickers = mean_ret.index.tolist()
        
        for t in valid_tickers:
            r = float(mean_ret[t])
            v = float(vol[t])
            if v > 0: # Avoid division by zero
                metrics.append({
                    "Ticker": t,
                    "Return": round(r, 4),
                    "Risk": round(v, 4),
                    "Sharpe": round((r - rf) / v, 4)
                })
        
        with open(METRICS_FILE, "w") as f:
            json.dump(metrics, f, indent=4)
            
        print(f"✅ Created {METRICS_FILE} with {len(metrics)} assets.")
        
    except Exception as e:
        print(f"Error creating JSON: {e}")
        # Create a dummy file so app doesn't crash loop
        with open(METRICS_FILE, "w") as f:
            json.dump([], f)

def calculate_portfolio_performance(weights, returns):
    weights = np.array(weights)
    mean_daily_return = returns.mean()
    cov_matrix = returns.cov()
    port_return = np.sum(mean_daily_return * weights) * TRADING_DAYS
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * TRADING_DAYS, weights)))
    return port_return, port_volatility

<<<<<<< HEAD
=======
def calculate_unsystematic_risk(weights, returns, market_ticker="^NSEI"):
    try:
        market_data = yf.download(market_ticker, start=returns.index[0], end=returns.index[-1], progress=False, auto_adjust=False)['Adj Close']
        market_ret = market_data.pct_change(fill_method=None).dropna()
        
        common_dates = returns.index.intersection(market_ret.index)
        port_daily_ret = returns.loc[common_dates].dot(weights)
        mkt_daily_ret = market_ret.loc[common_dates]
        
        covariance = np.cov(port_daily_ret, mkt_daily_ret)[0][1]
        market_variance = np.var(mkt_daily_ret)
        beta = covariance / market_variance
        
        total_variance = np.var(port_daily_ret)
        systematic_variance = (beta ** 2) * market_variance
        unsystematic_variance = total_variance - systematic_variance
        
        return {
            "Total Risk": np.sqrt(total_variance) * np.sqrt(TRADING_DAYS),
            "Systematic Risk": np.sqrt(systematic_variance) * np.sqrt(TRADING_DAYS),
            "Unsystematic Risk": np.sqrt(unsystematic_variance) * np.sqrt(TRADING_DAYS),
            "Beta": beta
        }
    except:
        # Fallback if market data fails
        total_vol = returns.dot(weights).std() * np.sqrt(TRADING_DAYS)
        return {
            "Total Risk": total_vol,
            "Systematic Risk": 0.0,
            "Unsystematic Risk": total_vol,
            "Beta": 1.0
        }

>>>>>>> 248f8fec53b4d47b47c5453e7a885e87a51fdf58
def get_efficient_frontier(returns, num_portfolios=200):
    mean_ret = returns.mean() * TRADING_DAYS
    cov_mat = returns.cov() * TRADING_DAYS
    num_assets = len(returns.columns)
    results = []
    for _ in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        p_ret = np.sum(mean_ret * weights)
        p_vol = np.sqrt(np.dot(weights.T, np.dot(cov_mat, weights)))
        results.append({"Return": p_ret, "Risk": p_vol, "Sharpe": (p_ret - 0.06) / p_vol})
    return pd.DataFrame(results)

def rank_candidates_by_risk_reduction(current_returns, candidate_tickers, candidate_data):
    current_weights = np.ones(current_returns.shape[1]) / current_returns.shape[1]
    _, current_vol = calculate_portfolio_performance(current_weights, current_returns)
    rankings = []
    
    for ticker in candidate_tickers:
        if ticker in current_returns.columns: continue
        # FIX: fill_method=None
        cand_ret = candidate_data[ticker].pct_change(fill_method=None).dropna()
        
        common_dates = current_returns.index.intersection(cand_ret.index)
        if len(common_dates) < 50: continue
        
        combined = current_returns.loc[common_dates].copy()
        combined[ticker] = cand_ret.loc[common_dates]
        
        n = combined.shape[1]
        new_w = np.array([0.9/(n-1)]*(n-1) + [0.1])
        _, new_vol = calculate_portfolio_performance(new_w, combined)
        
        rankings.append({
            "Ticker": ticker, 
            "Risk Reduction": current_vol - new_vol,
            "New Risk": new_vol, 
            "Correlation": combined.corr().iloc[:-1, -1].mean()
        })
    return pd.DataFrame(rankings).sort_values("Risk Reduction", ascending=False)
<<<<<<< HEAD


def calculate_unsystematic_risk(weights, returns, market_ticker="^NSEI"):
    """
    Decomposes risk into Systematic (Market) and Unsystematic (Specific).
    """
    try:
        # 1. Fetch Market Data (NIFTY 50)
        # Ensure we cover the full date range of the user's returns
        start_date = returns.index[0].strftime('%Y-%m-%d')
        end_date = returns.index[-1].strftime('%Y-%m-%d')
        
        market_data = yf.download(
            market_ticker, 
            start=start_date, 
            end=end_date, 
            progress=False, 
            auto_adjust=False,
            threads=True
        )['Adj Close']
        
        # Calculate Market Returns
        market_ret = market_data.pct_change(fill_method=None).dropna()
        
        # 2. Align Data (Intersection of dates)
        common_dates = returns.index.intersection(market_ret.index)
        
        if len(common_dates) < 10:
            print("⚠️ Warning: Not enough common dates between Portfolio and Market.")
            return {
                "Total Risk": returns.dot(weights).std() * np.sqrt(TRADING_DAYS),
                "Systematic Risk": 0.0,
                "Unsystematic Risk": returns.dot(weights).std() * np.sqrt(TRADING_DAYS),
                "Beta": 0.0
            }

        # Filter both series to common dates
        port_daily_ret = returns.loc[common_dates].dot(weights)
        mkt_daily_ret = market_ret.loc[common_dates]
        
        # 3. Calculate Beta
        covariance = np.cov(port_daily_ret, mkt_daily_ret)[0][1]
        market_variance = np.var(mkt_daily_ret)
        
        if market_variance == 0:
            beta = 0
        else:
            beta = covariance / market_variance
        
        # 4. Decompose Variance
        total_variance = np.var(port_daily_ret)
        systematic_variance = (beta ** 2) * market_variance
        unsystematic_variance = max(0, total_variance - systematic_variance) # Ensure non-negative
        
        return {
            "Total Risk": np.sqrt(total_variance) * np.sqrt(TRADING_DAYS),
            "Systematic Risk": np.sqrt(systematic_variance) * np.sqrt(TRADING_DAYS),
            "Unsystematic Risk": np.sqrt(unsystematic_variance) * np.sqrt(TRADING_DAYS),
            "Beta": beta
        }
        
    except Exception as e:
        print(f"Error in Risk Calc: {e}")
        # Fallback: Treat all risk as Total Risk
        total_vol = returns.dot(weights).std() * np.sqrt(TRADING_DAYS)
        return {
            "Total Risk": total_vol,
            "Systematic Risk": 0.0,
            "Unsystematic Risk": total_vol,
            "Beta": 0.0
        }

=======
>>>>>>> 248f8fec53b4d47b47c5453e7a885e87a51fdf58
