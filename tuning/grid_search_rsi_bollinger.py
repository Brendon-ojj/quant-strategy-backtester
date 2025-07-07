from strategies.RSIBollingerStrategy import RSIBollingerStrategy
from backtester.backtester import Backtester
import pandas as pd
import yfinance as yf
import itertools

# Parameter ranges
lookback_values = [5, 10, 15]
rsi_window_values = [10, 14, 20]
bb_window_values = [10, 20]
bb_std_values = [1.5, 2.0, 2.5]

# Store results
results_list = []

df = yf.download("GC=F", start="2022-01-01", end="2023-12-31")

# Grid search loop
for lookback, rsi_window, bb_window, bb_std in itertools.product(
        lookback_values, rsi_window_values, bb_window_values, bb_std_values
):
    strategy_params = {
        'lookback': lookback,
        'rsi_window': rsi_window,
        'window': bb_window,
        'num_std': bb_std
    }

    backtest = Backtester(
        data=df,
        strategy_cls=RSIBollingerStrategy,
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
        'bb_window': bb_window,
        'bb_std': bb_std,
        'final_value': round(float(results['final_value']), 2),
        'total_return': round(float(results['total_return']) * 100, 2),
        'win_rate': round(float(results['win_rate']) * 100, 2),
        'sharpe_ratio': round(float(results['sharpe_ratio']), 2),
        'total_trades': sum(1 for t in results['trades'] if t[0] in ['sell', 'take_profit', 'stop_loss'])
    })

# Create DataFrame
results_df = pd.DataFrame(results_list)

# Rename columns for display
results_df.rename(columns={
    'lookback': 'Lookback',
    'rsi_window': 'RSI Window',
    'bb_window': 'BB Window',
    'bb_std': 'BB Std',
    'final_value': 'Final Value',
    'total_return': 'Total Return (%)',
    'win_rate': 'Win Rate (%)',
    'sharpe_ratio': 'Sharpe',
    'total_trades': 'Trades'
}, inplace=True)

# Show top 10 by return
print(results_df.sort_values(by='Total Return (%)', ascending=False).head(10))
