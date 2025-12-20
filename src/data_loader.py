import yfinance as yf
import pandas as pd

def fetch_market_data(tickers, start_date="2023-01-01", end_date=None):
    if not tickers:
        return pd.DataFrame()
    
    try:
        # Download with threads to speed up, ignore missing to prevent crashes
        data = yf.download(
            tickers, 
            start=start_date, 
            end=end_date, 
            auto_adjust=False, 
            threads=True,
            ignore_tz=True # Helps with some delisted timezone errors
        )['Adj Close']
        
        # If only one ticker found, convert Series to DF
        if isinstance(data, pd.Series):
            data = data.to_frame()
            data.columns = tickers
            
        # Drop columns that are entirely NaN (failed downloads)
        data = data.dropna(axis=1, how='all')
        
        return data.dropna()
        
    except Exception as e:
        print(f"Error downloading data: {e}")
        return pd.DataFrame()

def fetch_fundamentals(tickers):
    data = []
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            data.append({
                "Ticker": t,
                "P/E Ratio": info.get('trailingPE', None),
                "Div Yield": (info.get('dividendYield', 0) or 0) * 100
            })
        except:
            data.append({"Ticker": t, "P/E Ratio": None, "Div Yield": 0})
    
    return pd.DataFrame(data)
