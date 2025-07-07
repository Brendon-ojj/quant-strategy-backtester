import yfinance as yf
from backtester.backtester import Backtester
from strategies.sma_crossover import SMACrossoverStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.rsi_sma_combo import RSISMACrossoverStrategy
from strategies.macd_crossover import MACDCrossoverStrategy
from strategies.bollinger_breakout import BollingerBreakoutStrategy
from strategies.high_low_breakout import HighLowBreakoutStrategy
from strategies.rsi_divergence import RSIDivergenceStrategy
from strategies.RSIBollingerStrategy import RSIBollingerStrategy
import pandas as pd

strategies_to_test = [
    ("SMA Only", SMACrossoverStrategy, {'short_window': 20, 'long_window': 50}),
    ("RSI Only", RSIStrategy, {'rsi_window': 14}),
    ("RSI + SMA", RSISMACrossoverStrategy, {'short_window': 20, 'long_window': 50, 'rsi_window': 14}),
    ("Bollinger Breakout", BollingerBreakoutStrategy, {
        'window': 20,
        'num_std': 2
    }),
    ("MACD Crossover Strategy", MACDCrossoverStrategy, {
        'fast': 12,
        'slow': 26,
        'signal': 9
    }),
    ("HighLow Breakout", HighLowBreakoutStrategy, {'lookback_window': 20, 'buffer_pct': 0.002}),
    ("RSI Divergence", RSIDivergenceStrategy, {'rsi_window': 14, 'lookback': 5}),
    ("RSI Bollinger Strategy", RSIBollingerStrategy, {
            'lookback': 10,
            'rsi_window': 14,
            'window': 20,
            'num_std': 2.0
        }),
]

strategies_to_test_df = pd.DataFrame(strategies_to_test, columns=["Name", "Class", "Params"])

tickers = ["AAPL", "NVDA", "TSLA", "GC=F", "PLTR"]

results_summary = []

for ticker in tickers:
    print(f"\n📊 Testing on {ticker}")
    df = yf.download(ticker, start="2022-01-01", end="2023-12-31")

    for name, strategy_cls, params in strategies_to_test:
        backtest = Backtester(
            data=df,
            strategy_cls=strategy_cls,
            strategy_kwargs=params,
            initial_cash=100000,
            allocation_pct=0.1,
            stop_loss_pct=0.05,
            take_profit_pct=0.1
        )
        results = backtest.run()

        results_summary.append({
            'ticker': ticker,
            'strategy': name,
            'final_value': float(results['final_value']),
            'total_return': float(results['total_return']),
            'win_rate': float(results['win_rate']),
            'sharpe_ratio': float(results['sharpe_ratio']),
            'total_trades': sum(1 for t in results['trades'] if t[0] in ['sell', 'take_profit', 'stop_loss'])
        })

# Sort by total return (descending)
sorted_results = sorted(results_summary, key=lambda x: x['total_return'], reverse=True)

# Filter: at least 3 trades and win rate >= 50%
filtered_results = [
    res for res in sorted_results
    if res['total_trades'] >= 3 and res['win_rate'] >= 0.5
]

print("\n✅ Filtered Strategy Leaderboard (≥ 3 Trades & Win Rate ≥ 50%):")
for i, res in enumerate(filtered_results, 1):
    print(f"{i}. [{res['ticker']}] {res['strategy']}: {res['total_return'] * 100:.2f}% return, "
          f"Win Rate: {res['win_rate'] * 100:.2f}%, Sharpe: {res['sharpe_ratio']:.2f}, "
          f"Trades: {res['total_trades']}")

