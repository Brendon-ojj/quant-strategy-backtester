# backtester/backtester.py

import pandas as pd
from quant_bot.utils.metrics import (
    calculate_sharpe_ratio,
    calculate_max_drawdown,
    calculate_win_rate,
    calculate_profit_factor
)

class Backtester:
    def __init__(self, data, strategy_cls, strategy_kwargs={}, initial_cash=100000, allocation_pct=0.1,
                 stop_loss_pct=0.05, take_profit_pct=0.1):

        """
              Initialize the backtester.

              Parameters:
              - data: OHLCV DataFrame
              - strategy_cls: strategy class to instantiate
              - strategy_kwargs: arguments for the strategy (e.g. windows)
              - initial_cash: starting capital
              - allocation_pct: % of cash to use per trade
              - stop_loss_pct: % drop from entry price to trigger stop-loss
              - take_profit_pct: % rise from entry price to trigger take-profit
              """

        self.data = data.copy()
        self.strategy = strategy_cls(data, **strategy_kwargs)
        self.initial_cash = initial_cash
        self.allocation_pct = allocation_pct
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct

        self.equity_curve = []
        self.position = 0
        self.cash = initial_cash
        self.portfolio_value = initial_cash
        self.trades = []

        self.entry_price = None  # track for SL/TP

    def run(self):
        """
        Execute the backtest using the strategy’s signals.
        Applies stop-loss and take-profit exit logic.
        """
        signals = self.strategy.generate_signals()
        prices = self.data['Close'].values

        for i, signal in enumerate(signals):
            price = prices[i]
            if pd.isna(price):
                self.equity_curve.append(self.portfolio_value)
                continue

            # If in position, check stop-loss or take-profit first
            if self.position > 0 and self.entry_price is not None:
                if price <= self.entry_price * (1 - self.stop_loss_pct):
                    # Trigger stop-loss
                    self.cash += self.position * price
                    self.trades.append(('stop_loss', i, price, self.position))
                    self.position = 0
                    self.entry_price = None

                elif price >= self.entry_price * (1 + self.take_profit_pct):
                    # Trigger take-profit
                    self.cash += self.position * price
                    self.trades.append(('take_profit', i, price, self.position))
                    self.position = 0
                    self.entry_price = None

            # Handle new signal
            if signal == 'buy' and self.cash > 0 and self.position == 0:
                allocation = self.cash * self.allocation_pct
                shares_to_buy = allocation // price
                if shares_to_buy > 0:
                    cost = shares_to_buy * price
                    self.cash -= cost
                    self.position += shares_to_buy
                    self.entry_price = price
                    self.trades.append(('buy', i, price, shares_to_buy))

            elif signal == 'sell' and self.position > 0:
                proceeds = self.position * price
                self.cash += proceeds
                self.trades.append(('sell', i, price, self.position))
                self.position = 0
                self.entry_price = None

            self.portfolio_value = self.cash + self.position * price
            self.equity_curve.append(self.portfolio_value)

        return self.get_summary()

    def get_summary(self):
        """
        Return a summary of the backtest.
        Includes final value, return, trades, and equity curve.
        """
        total_return = (self.portfolio_value - self.initial_cash) / self.initial_cash
        return {
            'initial_cash': float(self.initial_cash),
            'final_value': float(self.portfolio_value),
            'total_return': float(total_return),
            'trades': self.trades,
            'equity_curve': self.equity_curve,
            'sharpe_ratio': float(calculate_sharpe_ratio(self.equity_curve)),
            'max_drawdown': float(calculate_max_drawdown(self.equity_curve)),
            'win_rate': float(calculate_win_rate(self.trades)),
            'profit_factor': float(calculate_profit_factor(self.trades))
        }