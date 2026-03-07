# Web Backtesting App (No CSV Upload)

This project includes a browser-based backtester that fetches historical stock data automatically and runs your strategy in the page.

## How to run

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Features included

- Data fetching without manual CSV uploads
- Multi-endpoint fetch fallback (several proxy routes + direct attempt) for better reliability
- Ticker autocomplete suggestions for common US symbols
- Quick timeframe buttons: `1M`, `3M`, `6M`, `1Y`, `3Y`, `5Y`
- Strategy options:
  - SMA crossover
  - Breakout
  - RSI mean reversion
- Advanced variable coverage controls:
  - Direction mode (long-only / long-short)
  - Fast/slow/RSI thresholds
  - Position size %, leverage, fees, slippage
  - Stop loss / take profit / trailing stop
  - Min hold bars / max hold bars / cooldown bars
  - Trend and volume filters
- Benchmarking:
  - Buy & hold benchmark equity line
  - Strategy vs benchmark return and outperformance cards
- Exports:
  - `Export Trades CSV`
  - `Export Equity CSV`
- Optimizer:
  - Brute-force parameter search across broad variable ranges
  - Optional scope to test all included strategies
  - One-click `Run All Variables Test` button for a full preset search
  - Rank by outperformance, total return, or Sharpe
  - Show top combinations and apply best result to form
- Market discovery helper:
  - Top 10 most active stocks from the last 7 trading days
  - Ranked by average daily dollar volume from a liquid-symbol watchlist

## Notes

- This is a lightweight starter for educational/personal use.
- "Every possible variable" is not literally infinite in practice, but this UI now covers a much broader, practical set of strategy and execution variables.
- Brute-force combinations can explode quickly; optimizer uses a safety cap and you should narrow ranges thoughtfully.
- The active-stock panel is based on a curated universe, not the entire market universe.
- Real-world trading requires stronger data validation, corporate actions handling, realistic fills, and risk controls.
