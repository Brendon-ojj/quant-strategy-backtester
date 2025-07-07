# main.py

import pandas as pd
from backtester.backtester import Backtester
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import csv
import matplotlib.dates as mdates
from strategies.bollinger_breakout import BollingerBreakoutStrategy

# Define export path
export_path = "trades_output.csv"

# 1. Load real data (assumes OHLCV format)
df = yf.download("NVDA", start="2020-01-01", end="2025-01-01")

# 2. Initialize and run backtester
backtest = Backtester(
    data=df,
    strategy_cls=BollingerBreakoutStrategy,
    strategy_kwargs={
        'window': 20,
        'num_std': 2
    },
    initial_cash=100000,
    allocation_pct=0.1,
    stop_loss_pct=0.05,
    take_profit_pct=0.1
)

results = backtest.run()

buy_indices = []
sell_indices = []
prices = df['Close'].values

for trade in results['trades']:
    if trade[0] in ['buy']:
        buy_indices.append(trade[1])
    elif trade[0] in ['sell', 'take_profit', 'stop_loss']:
        sell_indices.append(trade[1])

# 3. Print summary
print("\n--- Backtest Results ---")
print(f"Initial Cash: ${results['initial_cash']:.2f}")
print(f"Final Value: ${results['final_value']:.2f}")
print(f"Total Return: {results['total_return']*100:.2f}%")
print(f"Total Trades: {len(results['trades'])}")
print(f"Win Rate: {results['win_rate']*100:.2f}%")
print(f"Profit Factor: {results['profit_factor']:.2f}")
print(f"Max Drawdown: {results['max_drawdown']*100:.2f}%")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")

# Open CSV file for writing
with open(export_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['Type', 'Index', 'Price', 'Shares'])

    # Write each trade row
    for trade in results['trades']:
        # Unpack trade tuple and flatten any arrays (for safety)
        trade_type = trade[0]
        index = int(trade[1])
        price = float(trade[2][0]) if isinstance(trade[2], np.ndarray) else float(trade[2])
        shares = float(trade[3][0]) if isinstance(trade[3], np.ndarray) else float(trade[3])
        writer.writerow([trade_type, index, price, shares])

print(f"\n📁 Trades exported to: {export_path}")

# 4. Plot equity curve
dates = df.index  # <-- this gives real timestamps

plt.figure(figsize=(14, 6))
plt.plot(dates, prices, label="Price")

# Mark trades using actual dates
plt.scatter([dates[i] for i in buy_indices], np.array(prices)[buy_indices], marker='^', color='green', label='Buy', zorder=5)
plt.scatter([dates[i] for i in sell_indices], np.array(prices)[sell_indices], marker='v', color='red', label='Sell', zorder=5)

# Format the x-axis as dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()  # Rotate date labels nicely

plt.title("Price Chart with Buy/Sell Points")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()