import os
from bitget.client import BitgetClient
from .exchange_base import ExchangeBase
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

class Bitget(ExchangeBase):
    def __init__(self, account_name, exchange_name, api_key, api_secret):
        super().__init__(account_name)
        self.client = BitgetClient(api_key, api_secret)

    def get_balance(self):
        """Get the balance of assets from the Bitget account."""
        balance_data = self.client.get_balance()
        return {balance["currency"]: float(balance["available"]) for balance in balance_data if float(balance["available"]) > 0}

    def get_prices(self):
        """Get the prices of assets on Bitget."""
        ticker_data = self.client.get_tickers()
        return {ticker["symbol"]: float(ticker["price"]) for ticker in ticker_data}

    def buy(self, asset, amount):
        """Buy the asset with the given amount."""
        symbol = asset + "USDT"
        self.client.place_order(symbol, "buy", amount)
        print(f"Placed buy order for {amount} of {asset} on Bitget.")

    def sell(self, asset, amount):
        """Sell the asset with the given amount."""
        symbol = asset + "USDT"
        self.client.place_order(symbol, "sell", amount)
        print(f"Placed sell order for {amount} of {asset} on Bitget.")
