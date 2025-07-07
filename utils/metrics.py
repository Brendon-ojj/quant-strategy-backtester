# utils/metrics.py

import numpy as np

def calculate_sharpe_ratio(equity_curve, risk_free_rate=0.0):
    """
    Calculates the annualized Sharpe Ratio:
    (mean return - risk-free rate) / std deviation of returns

    Parameters:
    - equity_curve: list of portfolio values over time
    - risk_free_rate: usually 0 for short-term testing

    Returns:
    - Sharpe ratio
    """
    # Daily returns from equity curve
    equity_curve = np.array(equity_curve).flatten()  # ensure 1D array
    returns = np.diff(equity_curve) / equity_curve[:-1]

    # Excess return = return - risk-free rate
    excess_returns = returns - risk_free_rate

    # Avoid division by zero
    if np.std(excess_returns) == 0:
        return 0

    # Annualized Sharpe ratio (√252 for daily data)
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)


def calculate_max_drawdown(equity_curve):
    """
    Calculates the max drawdown (largest % drop from peak to trough)

    Parameters:
    - equity_curve: list of portfolio values

    Returns:
    - max drawdown as a negative decimal (e.g. -0.12 for -12%)
    """
    equity_curve = np.array(equity_curve)
    # Track all-time highs up to each point
    peaks = np.maximum.accumulate(equity_curve)

    # Drop from peak at each time step
    drawdowns = (equity_curve - peaks) / peaks

    return drawdowns.min()


def calculate_win_rate(trades):
    """
    Calculates % of profitable trades

    Parameters:
    - trades: list of (type, index, price, shares)

    Returns:
    - win rate as decimal (0.6 = 60%)
    """
    wins = 0
    total = 0

    for i in range(len(trades)):
        if trades[i][0] in ('sell', 'stop_loss', 'take_profit'):
            # Look back to find the most recent buy
            buy_price = None
            for j in range(i - 1, -1, -1):
                if trades[j][0] == 'buy':
                    buy_price = trades[j][2]  # Buy price
                    break

            if buy_price:
                sell_price = trades[i][2]
                if sell_price > buy_price:
                    wins += 1
                total += 1

    return wins / total if total > 0 else 0


def calculate_profit_factor(trades):
    """
    Calculates profit factor = total profit / total loss

    Parameters:
    - trades: list of (type, index, price, shares)

    Returns:
    - profit factor (float, or inf if no losses)
    """
    profit = 0
    loss = 0

    for i in range(len(trades)):
        if trades[i][0] in ('sell', 'stop_loss', 'take_profit'):
            buy_price = None
            shares = trades[i][3]

            # Find the most recent corresponding buy
            for j in range(i - 1, -1, -1):
                if trades[j][0] == 'buy':
                    buy_price = trades[j][2]
                    break

            if buy_price:
                pnl = (trades[i][2] - buy_price) * shares
                if pnl > 0:
                    profit += pnl
                else:
                    loss += abs(pnl)

    return profit / loss if loss > 0 else float('inf')
