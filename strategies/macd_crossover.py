# strategies/macd_crossover.py

import pandas as pd
from strategies.base_strategy import BaseStrategy

class MACDCrossoverStrategy(BaseStrategy):
    """
    MACD Crossover Strategy:
    Buy when MACD line crosses above signal line
    Sell when MACD line crosses below signal line
    """

    def __init__(self, data, fast=10, slow=35, signal=12):
        super().__init__(data)
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def generate_signals(self):
        df = self.data.copy()

        # Calculate MACD and Signal Line
        df['EMA_fast'] = df['Close'].ewm(span=self.fast, adjust=False).mean()
        df['EMA_slow'] = df['Close'].ewm(span=self.slow, adjust=False).mean()
        df['MACD'] = df['EMA_fast'] - df['EMA_slow']
        df['Signal'] = df['MACD'].ewm(span=self.signal, adjust=False).mean()

        # Generate Buy/Sell Signals
        signals = ['hold'] * len(df)

        for i in range(1, len(df)):
            prev_macd = df['MACD'].iloc[i - 1]
            prev_signal = df['Signal'].iloc[i - 1]
            curr_macd = df['MACD'].iloc[i]
            curr_signal = df['Signal'].iloc[i]

            if curr_macd > curr_signal and prev_macd <= prev_signal:
                signals[i] = 'buy'
            elif curr_macd < curr_signal and prev_macd >= prev_signal:
                signals[i] = 'sell'
            else:
                signals[i] = 'hold'

        self.signals = signals
        return signals
