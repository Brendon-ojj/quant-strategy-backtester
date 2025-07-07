import itertools
import pandas as pd
import yfinance as yf
from backtester.backtester import Backtester
from strategies.rsi_divergence import RSIDivergenceStrategy

# Define search space
lookback_values = [10, 15, 20, 25]
rsi_window_values = [10, 14, 20]

# Asset to test
ticker = "NVDA"
df = yf.download(ticker, start="2022-01-01", end="2023-12-31")

# Store all results
results_list = []

# Grid search over all parameter combinations
for lookback, rsi_window in itertools.product(lookback_values, rsi_window_values):
    strategy_params = {
        'lookback': lookback,
        'rsi_window': rsi_window
    }

    backtest = Backtester(
        data=df,
        strategy_cls=RSIDivergenceStrategy,
        strategy_kwargs=strategy_params,
        initial_cash=100000,
        allocation_pct=0.1,
        stop_loss_pct=0.05,
        take_profit_pct=0.1
    )

    results = backtest.run()

    results_list.append({
        'lookback': lookback,
        'rsi_window': rsi_window,
        'final_value': round(float(results['final_value']), 2),
        'total_return': round(float(results['total_return']) * 100, 2),  # Convert to %
        'win_rate': round(float(results['win_rate']) * 100, 2),  # Convert to %
        'sharpe_ratio': round(float(results['sharpe_ratio']), 2),
        'total_trades': sum(1 for t in results['trades'] if t[0] in ['sell', 'take_profit', 'stop_loss'])
    })

# Convert to DataFrame and sort
results_df = pd.DataFrame(results_list)
results_df = results_df.sort_values(by='total_return', ascending=False)

results_df.rename(columns={
    "lookback": "Lookback",
    "rsi_window": "RSI Window",
    "final_value": "Final Value",
    "total_return": "Total Return (%)",
    "win_rate": "Win Rate (%)",
    "sharpe_ratio": "Sharpe",
    "total_trades": "Trades"
}, inplace=True)

# Save to CSV and print top results
results_df.to_csv("tuned_rsi_divergence_results.csv", index=False)
print(results_df.head(10))
