import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

markets = {
    "S&P 500": "^GSPC",
    "Euro Stoxx 50": "^STOXX50E",
    "VIX": "^VIX",
    "EUR/USD": "EURUSD=X"
}

print("=" * 72)
print("CROSS-ASSET QUANT MARKET MONITOR")
print(datetime.now().strftime("%d %B %Y"))
print("=" * 72)

print(
    f"{'Asset':<16}"
    f"{'1D Ret':>10}"
    f"{'20D Mom':>10}"
    f"{'20D Vol':>10}"
    f"{'Z':>8}"
)

print("-" * 72)

for name, ticker in markets.items():

    data = yf.download(
        ticker,
        period="6mo",
        progress=False,
        auto_adjust=True
    )

    prices = data["Close"].squeeze()

    # Daily log returns
    returns = np.log(prices / prices.shift(1)).dropna()

    # Latest daily return
    daily_return = returns.iloc[-1] * 100

    # 20-day momentum
    momentum_20d = ((prices.iloc[-1] / prices.iloc[-21]) - 1) * 100

    # 20-day annualised realised volatility
    vol_20d = returns.tail(20).std() * np.sqrt(252) * 100

    # Z-score of latest daily return
    mean_20d = returns.tail(20).mean()
    std_20d = returns.tail(20).std()

    z_score = (returns.iloc[-1] - mean_20d) / std_20d

    print(
    f"{name:<16}"
    f"{daily_return:>9.2f}%"
    f"{momentum_20d:>9.2f}%"
    f"{vol_20d:>9.2f}%"
    f"{z_score:>8.2f}"
)

print("=" * 72)