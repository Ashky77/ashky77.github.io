from dataclasses import dataclass

import pandas as pd


@dataclass
class SmaCrossStrategy:
    fast: int = 20
    slow: int = 50

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        fast_ma = data["close"].rolling(self.fast, min_periods=self.fast).mean()
        slow_ma = data["close"].rolling(self.slow, min_periods=self.slow).mean()
        return (fast_ma > slow_ma).astype(int)
