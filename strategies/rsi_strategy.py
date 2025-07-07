# strategies/rsi_strategy.py

import pandas as pd
from strategies.base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    """
    RSI Strategy:
    Buy when RSI < 30 (oversold)
    Sell when RSI > 70 (overbought)
    """

    def __init__(self, data, rsi_window=14):
        super().__init__(data)
        self.rsi_window = rsi_window

    def calculate_rsi(self, prices):
        delta = prices.diff()

        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_window).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signals(self):
        df = self.data.copy()

        # Calculate RSI from Close prices
        df['RSI'] = self.calculate_rsi(df['Close'])

        signals = ['hold'] * len(df)

        for i in range(1, len(df)):
            rsi = df['RSI'].iloc[i]

            if rsi < 30:
                signals[i] = 'buy'
            elif rsi > 70:
                signals[i] = 'sell'
            else:
                signals[i] = 'hold'

        self.signals = signals
        return signals
