# strategies/rsi_sma_combo.py

import pandas as pd
from strategies.base_strategy import BaseStrategy

class RSISMACrossoverStrategy(BaseStrategy):
    """
    RSI + SMA Crossover Strategy:
    Buy only when RSI < 30 AND short SMA crosses above long SMA
    Sell only when RSI > 70 AND short SMA crosses below long SMA
    """

    def __init__(self, data, short_window=20, long_window=50, rsi_window=14):
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window
        self.rsi_window = rsi_window

    def calculate_rsi(self, prices):
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=self.rsi_window).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=self.rsi_window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def generate_signals(self):
        df = self.data.copy()

        df['SMA_short'] = df['Close'].rolling(window=self.short_window).mean()
        df['SMA_long'] = df['Close'].rolling(window=self.long_window).mean()
        df['RSI'] = self.calculate_rsi(df['Close'])

        signals = ['hold'] * len(df)

        for i in range(1, len(df)):
            sma_cross_up = (
                df['SMA_short'].iloc[i] > df['SMA_long'].iloc[i] and
                df['SMA_short'].iloc[i - 1] <= df['SMA_long'].iloc[i - 1]
            )
            sma_cross_down = (
                df['SMA_short'].iloc[i] < df['SMA_long'].iloc[i] and
                df['SMA_short'].iloc[i - 1] >= df['SMA_long'].iloc[i - 1]
            )
            rsi = df['RSI'].iloc[i]

            if sma_cross_up and rsi < 40:
                signals[i] = 'buy'
            elif sma_cross_down and rsi > 60:
                signals[i] = 'sell'
            else:
                signals[i] = 'hold'

        self.signals = signals
        return signals
