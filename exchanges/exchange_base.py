from abc import ABC, abstractmethod

class ExchangeBase(ABC):
    def __init__(self, account_name, exchange_name):
        self.account_name = account_name
        self.exchange_name = exchange_name

    @abstractmethod
    def get_balance(self):
        """Retrieve account balances."""
        pass

    @abstractmethod
    def get_prices(self):
        """Retrieve the prices of assets on the exchange."""
        pass

    @abstractmethod
    def buy(self, asset, amount):
        """Execute a buy order for the asset."""
        pass

    @abstractmethod
    def sell(self, asset, amount):
        """Execute a sell order for the asset."""
        pass
