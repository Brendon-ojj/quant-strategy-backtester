# 🧠 Quant Strategy Backtester

A modular Python framework for backtesting and tuning technical trading strategies. Built from scratch without external backtesting libraries to learn core algorithmic logic and trading system design.

## 🔍 Project Overview

This project implements and compares multiple trading strategies using historical data from Yahoo Finance. Each strategy can be tuned using grid search, evaluated across multiple assets, and ranked by key performance metrics.

## 💡 Implemented Strategies

- **SMA Crossover**: Classic short vs long moving average.
- **RSI Strategy**: Momentum-based trading using Relative Strength Index.
- **MACD Crossover**: Signal-line crossover using MACD.
- **Bollinger Breakout**: Mean-reversion trades based on Bollinger Bands.
- **RSI Divergence**: Detects bullish/bearish divergence patterns.
- **RSI + SMA Combo**: Hybrid filter for confluence-based entries.
- **RSI Bollinger Strategy**: Custom strategy combining RSI divergence and Bollinger Band extremes.

## ⚙️ Features

- ✅ Modular strategy class architecture
- 🔁 Grid search tuning for optimal parameters
- 💹 Backtester with configurable risk parameters (stop loss, take profit)
- 📈 Performance metrics: Total Return, Win Rate, Sharpe Ratio, Trades
- 📤 Exportable trade logs and tuning results (`.csv`)

## 📦 Folder Structure

quant_bot/
├── backtester/ # Core engine
├── strategies/ # Custom strategy implementations
├── tuning/ # Grid search scripts
├── utils/ # Config, reusable utilities
├── trades_output.csv # Sample trade log
├── strategy_tester.py # Batch tester & leaderboard

## 🚀 How to Run

1. **Install dependencies**
```bash
pip install -r requirements.txt
