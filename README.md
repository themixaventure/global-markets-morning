# Global Markets Morning Brief

A Python-based cross-asset market monitoring tool designed to generate concise, sales-oriented market briefs from public market data.

## Objective

The project simulates the preparation of a Global Markets morning brief for institutional clients.

It automatically monitors key indicators across:

- Equities
- Rates
- Foreign Exchange
- Volatility

The objective is to transform raw market data into a concise and readable cross-asset market overview.

## Markets Covered

| Asset Class | Market |
|---|---|
| Equities | S&P 500 |
| Equities | Euro Stoxx 50 |
| Volatility | VIX |
| Rates | US 10-Year Treasury Yield |
| FX | EUR/USD |

## Features

- Automatic market data retrieval
- Daily price and yield monitoring
- Daily percentage change calculation
- Cross-asset market overview
- Simple UP / DOWN market direction indicator

## Technologies

- Python
- pandas
- yfinance

## Example Output

GLOBAL MARKETS MORNING BRIEF

S&P 500          7718.60   -0.38%   DOWN  
Euro Stoxx 50    6392.93   +0.16%   UP  
VIX                14.53   +1.47%   UP  
US 10Y Yield        4.78   +0.46%   UP  
EUR/USD              1.16   +0.31%   UP  

## Project Development

This project is being progressively expanded to include market interpretation, cross-asset signals and sales-oriented market commentary.

## Disclaimer

This project is for educational purposes only and does not constitute investment advice.
