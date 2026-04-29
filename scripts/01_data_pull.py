
"""
WYNN Resorts - Daily price data pull


from that CSV without needing internet access — keeps analysis reproducible.
"""
import yfinance as yf
import numpy as np
import pandas as pd
from pathlib import Path

TICKER = "WYNN"
START_DATE = "2005-01-01"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

print(f"Downloading {TICKER} from {START_DATE} to today...")
data = yf.download(
    TICKER,
    start=START_DATE,
    auto_adjust=False,
    progress=False,
)

# yfinance sometimes returns multi-index columns - flatten if so
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

print(f"\nShape: {data.shape}")
print(f"Range: {data.index.min().date()}  ->  {data.index.max().date()}")
print("\nFirst rows:")
print(data.head(3))
print("\nLast rows:")
print(data.tail(3))

# Compute daily log returns from adjusted close
prices = data["Adj Close"].dropna()
log_returns = np.log(prices / prices.shift(1)).dropna()
log_returns.name = "log_return"

print("\n--- Daily log-return summary ---")
print(f"N observations:  {len(log_returns)}")
print(f"Years of data:   {len(log_returns)/252:.2f}")
print(f"Mean:            {log_returns.mean():.6f}")
print(f"Std dev:         {log_returns.std():.6f}")
print(f"Variance:        {log_returns.var():.6f}")
print(f"Skewness:        {log_returns.skew():.4f}")
print(f"Excess kurtosis: {log_returns.kurtosis():.4f}")
print(f"Min: {log_returns.min():.4f} on {log_returns.idxmin().date()}")
print(f"Max: {log_returns.max():.4f} on {log_returns.idxmax().date()}")

# Save
out = pd.DataFrame({
    "adj_close": prices,
    "log_return": log_returns,
}).dropna()
out_path = DATA_DIR / "wynn_daily.csv"
out.to_csv(out_path)
print(f"\nSaved {len(out)} rows -> {out_path}")