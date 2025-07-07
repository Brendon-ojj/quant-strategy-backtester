import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy

class RSIDivergenceStrategy(BaseStrategy):
    """
    RSI Divergence Strategy:
    Buy when price makes a lower low but RSI makes a higher low (bullish divergence)
    Sell when price makes a higher high but RSI makes a lower high (bearish divergence)
    """

    def __init__(self, data, rsi_window=14, lookback=5):
        super().__init__(data)
        self.rsi_window = rsi_window
        self.lookback = lookback

    def calculate_rsi(self, prices):
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=self.rsi_window).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=self.rsi_window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def is_local_min(self, series, i):
        val = series.iloc[i].item()
        left = series.iloc[i - 1].item()
        right = series.iloc[i + 1].item()
        return val < left and val < right

    def is_local_max(self, series, i):
        val = series.iloc[i].item()
        left = series.iloc[i - 1].item()
        right = series.iloc[i + 1].item()
        return val > left and val > right

    def generate_signals(self):
        df = self.data.copy()
        df['RSI'] = self.calculate_rsi(df['Close'])
        signals = ['hold'] * len(df)

        for i in range(self.lookback + 1, len(df) - 1):
            price_now = df['Close'].iloc[i]
            rsi_now = df['RSI'].iloc[i]

            # Look for divergence in the past `lookback` bars
            for j in range(1, self.lookback + 1):
                prev_idx = i - j  # Define prev_idx

                price_prev = df['Close'].iloc[prev_idx].item()
                rsi_prev = df['RSI'].iloc[prev_idx].item()
                price_now = df['Close'].iloc[i].item()
                rsi_now = df['RSI'].iloc[i].item()

                # Bullish divergence
                if self.is_local_min(df['Close'], prev_idx) and self.is_local_min(df['Close'], i):
                    if price_now < price_prev and rsi_now > rsi_prev:
                        signals[i] = 'buy'
                        break

                # Bearish divergence
                if self.is_local_max(df['Close'], prev_idx) and self.is_local_max(df['Close'], i):
                    if price_now > price_prev and rsi_now < rsi_prev:
                        signals[i] = 'sell'
                        break

        self.signals = signals
        return signals
