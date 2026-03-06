from pathlib import Path

from backtest_engine import BacktestEngine
from strategies import SmaCrossStrategy


def main() -> None:
    csv_path = Path("sample_ohlcv.csv")
    if not csv_path.exists():
        raise FileNotFoundError(
            "Expected sample_ohlcv.csv. Create one with columns: "
            "timestamp,open,high,low,close,volume"
        )

    engine = BacktestEngine()
    data = engine.load_ohlcv_csv(csv_path)
    strategy = SmaCrossStrategy(fast=20, slow=50)

    result = engine.run(data, strategy)
    print("Metrics:")
    for k, v in result.metrics.items():
        print(f"- {k}: {v:.4f}")

    result.equity_curve.to_csv("equity_curve.csv", index=False)
    result.trades.to_csv("trades.csv", index=False)
    print("Saved equity_curve.csv and trades.csv")


if __name__ == "__main__":
    main()
