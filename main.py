import yfinance as yf
from datetime import datetime

markets = {
    "S&P 500": "^GSPC",
    "Euro Stoxx 50": "^STOXX50E",
    "VIX": "^VIX",
    "US 10Y Yield": "^TNX",
    "EUR/USD": "EURUSD=X"
}

print("=" * 60)
print("GLOBAL MARKETS MORNING BRIEF")
print(datetime.now().strftime("%d %B %Y"))
print("=" * 60)

for name, ticker in markets.items():
    data = yf.download(ticker, period="5d", progress=False)

    if len(data) >= 2:
        previous_close = data["Close"].iloc[-2].item()
        latest_close = data["Close"].iloc[-1].item()

        change = ((latest_close / previous_close) - 1) * 100

        direction = "UP" if change > 0 else "DOWN"

        print(
            f"{name:<20}"
            f"{latest_close:>12.2f}"
            f"{change:>9.2f}%  "
            f"{direction}"
        )

print("=" * 60)
