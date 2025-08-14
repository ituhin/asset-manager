import os
from kucoin.client import Client
from .exchange_base import ExchangeBase
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

class KuCoin(ExchangeBase):
    def __init__(self, account_name, exchange_name, api_key, api_secret, api_passphrase):
        super().__init__(account_name, exchange_name)
        self.client = Client(api_key, api_secret, api_passphrase)

    def get_balance(self):
        """Get the balance of assets from the KuCoin account."""
        balance_data = self.client.get_account().get("data")
        return {balance["currency"]: float(balance["balance"]) for balance in balance_data if float(balance["balance"]) > 0}

    def get_prices(self):
        """Get the prices of assets on KuCoin."""
        ticker_data = self.client.get_tickers()
        return {ticker["symbol"]: float(ticker["last"]) for ticker in ticker_data["data"]}

    def buy(self, asset, amount):
        """Buy the asset with the given amount."""
        symbol = asset + "-USDT"
        self.client.create_market_order(symbol, Client.SIDE_BUY, size=amount)
        print(f"Placed buy order for {amount} of {asset} on KuCoin.")

    def sell(self, asset, amount):
        """Sell the asset with the given amount."""
        symbol = asset + "-USDT"
        self.client.create_market_order(symbol, Client.SIDE_SELL, size=amount)
        print(f"Placed sell order for {amount} of {asset} on KuCoin.")
