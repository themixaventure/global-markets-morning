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

print("=" * 82)
print("CROSS-ASSET QUANT MARKET MONITOR")
print(datetime.now().strftime("%d %B %Y"))
print("=" * 82)

print(
    f"{'Asset':<16}"
    f"{'1D Ret':>10}"
    f"{'20D Mom':>10}"
    f"{'20D Vol':>10}"
    f"{'Z':>8}"
    f"{'Signal':>12}"
)

print("-" * 82)

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

    # Latest daily log return
    daily_return = returns.iloc[-1] * 100

    # 20-day momentum
    momentum_20d = (
        (prices.iloc[-1] / prices.iloc[-21]) - 1
    ) * 100

    # 20-day annualized realized volatility
    recent_returns = returns.tail(20)

    vol_20d = (
        recent_returns.std()
        * np.sqrt(252)
        * 100
    )

    # Z-score of the latest daily return
    mean_20d = recent_returns.mean()
    std_20d = recent_returns.std()

    if std_20d != 0:
        z_score = (
            returns.iloc[-1] - mean_20d
        ) / std_20d
    else:
        z_score = 0

    # Simple standardized-return classification
    if z_score > 1:
        signal = "HIGH"
    elif z_score < -1:
        signal = "LOW"
    else:
        signal = "NORMAL"

    print(
        f"{name:<16}"
        f"{daily_return:>9.2f}%"
        f"{momentum_20d:>9.2f}%"
        f"{vol_20d:>9.2f}%"
        f"{z_score:>8.2f}"
        f"{signal:>12}"
    )

print("=" * 82)