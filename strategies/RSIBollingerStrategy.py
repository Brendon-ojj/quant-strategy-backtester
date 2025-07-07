from strategies.base_strategy import BaseStrategy
import pandas as pd


# df.rename(columns={
#     "lookback": "Lookback",
#     "rsi_window": "RSI Window",
#     "bb_window": "BB Window",
#     "bb_std": "BB Std Dev",
#     "final_value": "Final Value",
#     "total_return": "Total Return (%)",
#     "win_rate": "Win Rate (%)",
#     "sharpe_ratio": "Sharpe",
#     "total_trades": "Trades"
# }, inplace=True)

class RSIBollingerStrategy(BaseStrategy):
    def __init__(self, data, lookback, rsi_window, window, num_std):
        super().__init__(data)
        self.lookback = lookback
        self.rsi_window = rsi_window
        self.window = window
        self.num_std = num_std

    def calculate_rsi(self, prices):
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=self.rsi_window).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=self.rsi_window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def is_local_min(self, series, i):
        center = series.iloc[i].item()
        left = series.iloc[i - 1].item()
        right = series.iloc[i + 1].item()
        return center < left and center < right

    def is_local_max(self, series, i):
        center = series.iloc[i].item()
        left = series.iloc[i - 1].item()
        right = series.iloc[i + 1].item()
        return center > left and center > right

    def generate_signals(self):
        df = self.data.copy()

        # Bollinger Bands
        df['SMA'] = df['Close'].rolling(window=self.window).mean()
        df['STD'] = df['Close'].rolling(window=self.window).std()
        df['Upper'] = df['SMA'] + self.num_std * df['STD']
        df['Lower'] = df['SMA'] - self.num_std * df['STD']

        # RSI
        df['RSI'] = self.calculate_rsi(df['Close'])

        signals = ['hold'] * len(df)

        for i in range(self.lookback + 1, len(df) - 1):
            price_now = df['Close'].iloc[i].item()
            upper = float(df['Upper'].iloc[i])
            lower = float(df['Lower'].iloc[i])

            for j in range(1, self.lookback + 1):
                prev_idx = i - j

                # ✅ Skip invalid index access BEFORE using prev_idx
                if prev_idx <= 0 or i + 1 >= len(df):
                    continue

                price_prev = df['Close'].iloc[prev_idx].item()
                rsi_now = df['RSI'].iloc[i].item()
                rsi_prev = df['RSI'].iloc[prev_idx].item()

                # Buy: Price below lower band and bullish RSI divergence
                if (price_now < lower and
                    self.is_local_min(df['Close'], prev_idx) and
                    self.is_local_min(df['Close'], i) and
                    price_now > price_prev and rsi_now > rsi_prev):
                    signals[i] = 'buy'
                    break

                # Sell: Price above upper band and bearish RSI divergence
                if (price_now > upper and
                    self.is_local_max(df['Close'], prev_idx) and
                    self.is_local_max(df['Close'], i) and
                    price_now < price_prev and rsi_now < rsi_prev):
                    signals[i] = 'sell'
                    break

        self.signals = signals
        return signals
