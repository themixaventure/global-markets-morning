from datetime import datetime

markets = {
    "S&P 500": 0.72,
    "Euro Stoxx 50": 0.41,
    "VIX": -3.20,
    "US 10Y": 0.05,
    "EUR/USD": 0.28
}

print("=" * 45)
print("GLOBAL MARKETS MORNING BRIEF")
print(datetime.now().strftime("%d %B %Y"))
print("=" * 45)

for asset, change in markets.items():
    direction = "UP" if change > 0 else "DOWN"
    print(f"{asset:<20} {change:+.2f}%  {direction}")

print("=" * 45)
