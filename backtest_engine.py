from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from pathlib import Path
from typing import Protocol

import pandas as pd


class Strategy(Protocol):
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Return a position signal per bar (1 for long, 0 for flat)."""


@dataclass
class BacktestConfig:
    initial_cash: float = 10_000.0
    fee_bps: float = 1.0
    slippage_bps: float = 2.0


@dataclass
class BacktestResult:
    equity_curve: pd.DataFrame
    trades: pd.DataFrame
    metrics: dict[str, float]


class BacktestEngine:
    def __init__(self, config: BacktestConfig | None = None) -> None:
        self.config = config or BacktestConfig()

    @staticmethod
    def load_ohlcv_csv(path: str | Path) -> pd.DataFrame:
        data = pd.read_csv(path)
        required = {"timestamp", "open", "high", "low", "close", "volume"}
        missing = required - set(data.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)
        data = data.sort_values("timestamp").reset_index(drop=True)
        return data

    def run(self, data: pd.DataFrame, strategy: Strategy) -> BacktestResult:
        signals = strategy.generate_signals(data).fillna(0).clip(lower=0, upper=1)
        signals = signals.astype(int)

        position_prev = signals.shift(1).fillna(0)
        returns = data["close"].pct_change().fillna(0)

        turnover = (signals - position_prev).abs()
        total_cost_bps = self.config.fee_bps + self.config.slippage_bps
        cost = turnover * (total_cost_bps / 10_000)

        strat_returns = (position_prev * returns) - cost
        equity = self.config.initial_cash * (1 + strat_returns).cumprod()

        equity_curve = pd.DataFrame(
            {
                "timestamp": data["timestamp"],
                "close": data["close"],
                "signal": signals,
                "position": position_prev,
                "asset_return": returns,
                "strategy_return": strat_returns,
                "equity": equity,
            }
        )

        trades = self._extract_trades(data, signals)
        metrics = self._compute_metrics(strat_returns, equity)

        return BacktestResult(equity_curve=equity_curve, trades=trades, metrics=metrics)

    @staticmethod
    def _extract_trades(data: pd.DataFrame, signals: pd.Series) -> pd.DataFrame:
        signal_change = signals.diff().fillna(signals.iloc[0])
        entries = data.loc[signal_change == 1, ["timestamp", "close"]].rename(
            columns={"timestamp": "entry_time", "close": "entry_price"}
        )
        exits = data.loc[signal_change == -1, ["timestamp", "close"]].rename(
            columns={"timestamp": "exit_time", "close": "exit_price"}
        )

        n = min(len(entries), len(exits))
        entries = entries.iloc[:n].reset_index(drop=True)
        exits = exits.iloc[:n].reset_index(drop=True)

        if n == 0:
            return pd.DataFrame(columns=["entry_time", "entry_price", "exit_time", "exit_price", "pnl_pct"])

        trades = pd.concat([entries, exits], axis=1)
        trades["pnl_pct"] = (trades["exit_price"] - trades["entry_price"]) / trades["entry_price"]
        return trades

    @staticmethod
    def _compute_metrics(strat_returns: pd.Series, equity: pd.Series) -> dict[str, float]:
        total_return = (equity.iloc[-1] / equity.iloc[0]) - 1

        daily = strat_returns
        mean_daily = daily.mean()
        std_daily = daily.std(ddof=0)
        sharpe = 0.0 if std_daily == 0 else (mean_daily / std_daily) * sqrt(252)

        rolling_peak = equity.cummax()
        drawdown = (equity - rolling_peak) / rolling_peak
        max_drawdown = drawdown.min()

        win_rate = float((daily > 0).sum() / max((daily != 0).sum(), 1))

        return {
            "total_return": float(total_return),
            "sharpe": float(sharpe),
            "max_drawdown": float(max_drawdown),
            "win_rate": float(win_rate),
        }
