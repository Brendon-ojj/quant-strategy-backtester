# strategies/bollinger_breakout.py

import pandas as pd
from strategies.base_strategy import BaseStrategy

class BollingerBreakoutStrategy(BaseStrategy):
    """
    Bollinger Band Breakout Strategy:
    Buy when price closes above upper band (breakout)
    Sell when price closes below lower band (breakdown)
    """

    def __init__(self, data, window=20, num_std=2):
        super().__init__(data)
        self.window = window
        self.num_std = num_std

    def generate_signals(self):
        df = self.data.copy()

        # Calculate Bollinger Bands
        df['SMA'] = df['Close'].rolling(window=self.window).mean()
        df['STD'] = df['Close'].rolling(window=self.window).std()
        df['Upper'] = df['SMA'] + self.num_std * df['STD']
        df['Lower'] = df['SMA'] - self.num_std * df['STD']

        signals = ['hold'] * len(df)

        for i in range(1, len(df)):
            # Safely extract scalar values
            close_now = df['Close'].iloc[i].item()
            close_prev = df['Close'].iloc[i - 1].item()
            upper_now = df['Upper'].iloc[i].item()
            upper_prev = df['Upper'].iloc[i - 1].item()
            lower_now = df['Lower'].iloc[i].item()
            lower_prev = df['Lower'].iloc[i - 1].item()

            # Skip if any are NaN
            if any(pd.isna([close_now, close_prev, upper_now, upper_prev, lower_now, lower_prev])):
                continue

            if close_now > upper_now and close_prev <= upper_prev:
                signals[i] = 'buy'
            elif close_now < lower_now and close_prev >= lower_prev:
                signals[i] = 'sell'
            else:
                signals[i] = 'hold'

        self.signals = signals
        return signals
