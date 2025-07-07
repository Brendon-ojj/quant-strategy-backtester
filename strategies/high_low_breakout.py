# strategies/high_low_breakout.py

import pandas as pd
from strategies.base_strategy import BaseStrategy

class HighLowBreakoutStrategy(BaseStrategy):
    """
    Buy when price breaks above recent high.
    Sell when price breaks below recent low.
    """

    def __init__(self, data, lookback_window=20, buffer_pct=0.0):
        super().__init__(data)
        self.lookback_window = lookback_window
        self.buffer_pct = buffer_pct

    def generate_signals(self):
        df = self.data.copy()
        signals = ['hold'] * len(df)

        df['RecentHigh'] = df['Close'].rolling(window=self.lookback_window).max()
        df['RecentLow'] = df['Close'].rolling(window=self.lookback_window).min()

        for i in range(self.lookback_window, len(df)):
            prev_price = df['Close'].iloc[i - 1].item()
            price = df['Close'].iloc[i].item()
            high = df['High'].iloc[i - 1].item()
            low = df['Low'].iloc[i - 1].item()

            if prev_price <= high * (1 + self.buffer_pct) and price > high * (1 + self.buffer_pct):
                signals[i] = 'buy'
            elif prev_price >= low * (1 - self.buffer_pct) and price < low * (1 - self.buffer_pct):
                signals[i] = 'sell'
            else:
                signals[i] = 'hold'

        self.signals = signals
        return signals
