# strategies/base_strategy.py

class BaseStrategy:
    """
    Base class for all strategies.
    Every strategy must inherit this and implement `generate_signals`.
    """
    def __init__(self, data):
        self.data = data.copy()  # DataFrame with OHLCV
        self.signals = []

    def generate_signals(self):
        """
        To be implemented by strategy subclass.
        Must return a list of 'buy', 'sell', or 'hold' signals.
        """
        raise NotImplementedError("You must implement generate_signals()")

    def get_signals(self):
        return self.signals
