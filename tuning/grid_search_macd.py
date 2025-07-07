from strategies.macd_crossover import MACDCrossoverStrategy
from backtester.backtester import Backtester
import pandas as pd
import yfinance as yf
import itertools
pd.set_option("display.precision", 2)  # Round floats to 2 decimals
pd.set_option("display.expand_frame_repr", False)  # Print wide frames in one line


# Grid values
fast_values = [5, 8, 12]
slow_values = [20, 26, 30]
signal_values = [6, 9, 12]

# Store results
results_list = []

# Download data
df = yf.download("GC=F", start="2022-01-01", end="2023-12-31")

# Run all valid combinations (fast < slow)
for fast, slow, signal in itertools.product(fast_values, slow_values, signal_values):
    if fast >= slow:
        continue  # Skip invalid

    strategy_params = {
        'fast': fast,
        'slow': slow,
        'signal': signal
    }

    backtest = Backtester(
        data=df,
        strategy_cls=MACDCrossoverStrategy,
        strategy_kwargs=strategy_params,
        initial_cash=100000,
        allocation_pct=0.1,
        stop_loss_pct=0.05,
        take_profit_pct=0.1
    )

    results = backtest.run()

    results_list.append({
        'fast': fast,
        'slow': slow,
        'signal': signal,
        'final_value': round(float(results['final_value']), 2),
        'total_return': round(float(results['total_return']) * 100, 2),
        'win_rate': round(float(results['win_rate']) * 100, 2),
        'sharpe_ratio': round(float(results['sharpe_ratio']), 2),
        'total_trades': sum(1 for t in results['trades'] if t[0] in ['sell', 'take_profit', 'stop_loss'])
    })

# Convert and sort
df = pd.DataFrame(results_list)
df = df.sort_values(by='total_return', ascending=False)

# Optional: Rename columns
df.rename(columns={
    "fast": "Fast",
    "slow": "Slow",
    "signal": "Signal",
    "final_value": "Final Value",
    "total_return": "Total Return (%)",
    "win_rate": "Win Rate (%)",
    "sharpe_ratio": "Sharpe",
    "total_trades": "Trades"
}, inplace=True)

print(df.head(10))
df.to_csv("tuned_macd_results.csv", index=False)
