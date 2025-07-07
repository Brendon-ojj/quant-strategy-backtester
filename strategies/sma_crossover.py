# strategies/sma_crossover.py

import pandas as pd
from strategies.base_strategy import BaseStrategy

class SMACrossoverStrategy(BaseStrategy):
    """
    SMA Crossover Strategy:
    Buy when short-term SMA crosses above long-term SMA
    Sell when short-term SMA crosses below long-term SMA
    """

    def __init__(self, data, short_window=20, long_window=50):
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        df = self.data.copy()

        # Calculate short-term and long-term SMAs
        df['SMA_short'] = df['Close'].rolling(window=self.short_window).mean()
        df['SMA_long'] = df['Close'].rolling(window=self.long_window).mean()

        # Initialize signal list with 'hold'
        signals = ['hold'] * len(df)

        for i in range(1, len(df)):
            # If short SMA crosses above long SMA => BUY
            if df['SMA_short'].iloc[i] > df['SMA_long'].iloc[i] and df['SMA_short'].iloc[i - 1] <= df['SMA_long'].iloc[
                i - 1]:
                signals[i] = 'buy'

            # If short SMA crosses below long SMA => SELL
            elif df['SMA_short'].iloc[i] < df['SMA_long'].iloc[i] and df['SMA_short'].iloc[i - 1] >= df['SMA_long'].iloc[i - 1]:
                signals[i] = 'sell'

            # Else, keep holding
            else:
                signals[i] = 'hold'

        self.signals = signals
        return signals
