# Web Backtesting App (No CSV Upload)

This project includes a browser-based backtester in `backtester/index.html` that fetches historical stock data automatically and runs your strategy in the page.

## How to run

```bash
python3 -m http.server 8000
# open http://localhost:8000/backtester/
```

## Features included

- Data fetching without manual CSV uploads
- Ticker autocomplete suggestions for common US symbols
- Quick timeframe buttons: `1M`, `3M`, `6M`, `1Y`, `3Y`, `5Y`
- Strategy options:
  - SMA crossover
  - 20-day breakout (configurable lookback)
- Risk controls:
  - Stop loss (%)
  - Take profit (%)
- Benchmarking:
  - Buy & hold benchmark equity line
  - Strategy vs benchmark return and outperformance cards
- Exports:
  - `Export Trades CSV`
  - `Export Equity CSV`
- Metrics:
  - Total return
  - Sharpe ratio
  - Max drawdown
  - Win rate
  - Final equity

## Notes

- This is a lightweight starter for educational/personal use.
- Real-world trading requires stronger data validation, corporate actions handling, realistic fills, and risk controls.
