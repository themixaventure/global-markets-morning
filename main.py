import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime


# ==========================================================
# MARKET UNIVERSE
# ==========================================================

markets = {
    "S&P 500": "^GSPC",
    "Euro Stoxx 50": "^STOXX50E",
    "VIX": "^VIX",
    "EUR/USD": "EURUSD=X"
}


# ==========================================================
# CROSS-ASSET QUANT MARKET MONITOR
# ==========================================================

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

    log_returns = np.log(
        prices / prices.shift(1)
    ).dropna()

    daily_return = log_returns.iloc[-1] * 100

    momentum_20d = (
        prices.iloc[-1] / prices.iloc[-21] - 1
    ) * 100

    recent_returns = log_returns.tail(20)

    vol_20d = (
        recent_returns.std()
        * np.sqrt(252)
        * 100
    )

    mean_20d = recent_returns.mean()
    std_20d = recent_returns.std()

    if std_20d != 0:
        z_score = (
            log_returns.iloc[-1] - mean_20d
        ) / std_20d
    else:
        z_score = 0

    if z_score > 1:
        classification = "HIGH"
    elif z_score < -1:
        classification = "LOW"
    else:
        classification = "NORMAL"

    print(
        f"{name:<16}"
        f"{daily_return:>9.2f}%"
        f"{momentum_20d:>9.2f}%"
        f"{vol_20d:>9.2f}%"
        f"{z_score:>8.2f}"
        f"{classification:>12}"
    )

print("=" * 82)


# ==========================================================
# SIMPLE MOMENTUM BACKTEST - S&P 500
# ==========================================================

print()
print("SIMPLE 20D MOMENTUM BACKTEST - S&P 500")
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
momentum = (
    prices / prices.shift(20)
) - 1

# Trading signal
signal = np.where(
    momentum > 0,
    1,
    -1
)

signal = pd.Series(
    signal,
    index=prices.index
)

# Shift signal by one day to avoid look-ahead bias
position = signal.shift(1)

# Gross strategy returns
gross_strategy_returns = (
    position * returns
)

# ==========================================================
# TRANSACTION COSTS
# ==========================================================

# 5 basis points per unit of turnover
transaction_cost_bps = 5
transaction_cost = transaction_cost_bps / 10000

# Turnover:
# 0 if the position does not change
# 2 when moving from +1 to -1 or -1 to +1
turnover = position.diff().abs()

# Daily transaction cost
daily_cost = (
    turnover * transaction_cost
)

# Net strategy returns after costs
strategy_returns = (
    gross_strategy_returns - daily_cost
).dropna()


# ==========================================================
# PERFORMANCE STATISTICS
# ==========================================================

annual_return = (
    strategy_returns.mean() * 252
)

annual_vol = (
    strategy_returns.std()
    * np.sqrt(252)
)

if annual_vol != 0:
    sharpe_ratio = (
        annual_return / annual_vol
    )
else:
    sharpe_ratio = 0


# ==========================================================
# EQUITY CURVE
# ==========================================================

equity_curve = (
    1 + strategy_returns
).cumprod()


# ==========================================================
# MAXIMUM DRAWDOWN
# ==========================================================

running_max = equity_curve.cummax()

drawdown = (
    equity_curve / running_max
) - 1

max_drawdown = drawdown.min()


# ==========================================================
# HIT RATIO
# ==========================================================

hit_ratio = (
    strategy_returns > 0
).mean()


# ==========================================================
# TURNOVER
# ==========================================================

annual_turnover = (
    turnover.loc[strategy_returns.index].mean()
    * 252
)


# ==========================================================
# DISPLAY BACKTEST RESULTS
# ==========================================================

print(
    f"Annualized Return : "
    f"{annual_return * 100:>8.2f}%"
)

print(
    f"Annualized Vol    : "
    f"{annual_vol * 100:>8.2f}%"
)

print(
    f"Sharpe Ratio      : "
    f"{sharpe_ratio:>8.2f}"
)

print(
    f"Max Drawdown      : "
    f"{max_drawdown * 100:>8.2f}%"
)

print(
    f"Hit Ratio         : "
    f"{hit_ratio * 100:>8.2f}%"
)

print(
    f"Annual Turnover   : "
    f"{annual_turnover:>8.2f}x"
)

print(
    f"Transaction Cost  : "
    f"{transaction_cost_bps:>8.1f} bps"
)

print("=" * 60)


# ==========================================================
# BUY & HOLD BENCHMARK
# ==========================================================

benchmark_returns = returns.loc[
    strategy_returns.index
]

benchmark_curve = (
    1 + benchmark_returns
).cumprod()


# ==========================================================
# PERFORMANCE CHART
# ==========================================================

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    equity_curve.index,
    equity_curve,
    label="20D Momentum Strategy (Net)"
)

plt.plot(
    benchmark_curve.index,
    benchmark_curve,
    label="S&P 500 Buy & Hold"
)

plt.title(
    "20-Day Momentum Strategy vs S&P 500"
)

plt.xlabel("Date")

plt.ylabel("Growth of $1")

plt.legend()

plt.grid(
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "momentum_backtest.png",
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print()
print(
    "Chart saved as: momentum_backtest.png"
)