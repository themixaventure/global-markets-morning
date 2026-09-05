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

    returns = np.log(prices / prices.shift(1)).dropna()

    daily_return = returns.iloc[-1] * 100

    momentum_20d = (
        (prices.iloc[-1] / prices.iloc[-21]) - 1
    ) * 100

    recent_returns = returns.tail(20)

    vol_20d = (
        recent_returns.std()
        * np.sqrt(252)
        * 100
    )

    mean_20d = recent_returns.mean()
    std_20d = recent_returns.std()

    if std_20d != 0:
        z_score = (
            returns.iloc[-1] - mean_20d
        ) / std_20d
    else:
        z_score = 0

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


# ==========================================================
# SIMPLE MOMENTUM BACKTEST - S&P 500
# ==========================================================

print("\nSIMPLE 20D MOMENTUM BACKTEST - S&P 500")
print("=" * 60)

sp500 = yf.download(
    "^GSPC",
    period="5y",
    progress=False,
    auto_adjust=True
)

prices = sp500["Close"].squeeze()

# Daily simple returns
returns = prices.pct_change()

# 20-day momentum
momentum = prices / prices.shift(20) - 1

# Trading signal
# +1 = long
# -1 = short
signal = np.where(momentum > 0, 1, -1)

signal = pd.Series(
    signal,
    index=prices.index
)

# Shift signal by one day to avoid look-ahead bias
strategy_returns = signal.shift(1) * returns

# Remove missing observations
strategy_returns = strategy_returns.dropna()

# Performance statistics
annual_return = strategy_returns.mean() * 252

annual_vol = strategy_returns.std() * np.sqrt(252)

if annual_vol != 0:
    sharpe_ratio = annual_return / annual_vol
else:
    sharpe_ratio = 0

# Equity curve
equity_curve = (1 + strategy_returns).cumprod()

# Maximum drawdown
running_max = equity_curve.cummax()

drawdown = (
    equity_curve / running_max
) - 1

max_drawdown = drawdown.min()

# Hit ratio
hit_ratio = (
    strategy_returns > 0
).mean()

print(f"Annualized Return : {annual_return * 100:>8.2f}%")
print(f"Annualized Vol    : {annual_vol * 100:>8.2f}%")
print(f"Sharpe Ratio      : {sharpe_ratio:>8.2f}")
print(f"Max Drawdown      : {max_drawdown * 100:>8.2f}%")
print(f"Hit Ratio         : {hit_ratio * 100:>8.2f}%")

print("=" * 60)