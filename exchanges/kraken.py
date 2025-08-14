import os
from krakenex import API
from .exchange_base import ExchangeBase
from dotenv import load_dotenv

class Kraken(ExchangeBase):
    def __init__(self, account_name, exchange_name, api_key, api_secret):
        super().__init__(account_name, exchange_name)
        self.api = API()

        # Set API keys directly
        self.api.key = api_key
        self.api.secret = api_secret

        if os.getenv('EXCHANGE_SANDBOX', 'false').lower() == 'true':
            self.api.url = 'https://api.sandbox.kraken.com/0'
        else:
            self.api.url = 'https://api.kraken.com/0'

    def get_balance(self):
        """Get the balance of assets from the Kraken account."""
        balance_data = self.api.query_private("Balance")["result"]

        return {asset: float(amount) for asset, amount in balance_data.items() if float(amount) > 0}

    def get_prices(self):
        """Get the prices of all available trading pairs on Kraken."""
        # Fetch all available trading pairs from Kraken
        pairs_data = self.api.query_public("AssetPairs")["result"]
        
        # Extract the trading pairs from the response
        pairs = [pair for pair in pairs_data.keys()]
        #print(pairs)

        # Fetch prices for all pairs in one request
        ticker_data = self.api.query_public("Ticker", {"pair": ",".join(pairs)})["result"]
        
        prices = {}
        
        # Extract the last trade price for each pair
        for pair in pairs:
            if pair in ticker_data:
                last_trade_price = ticker_data[pair]["c"][0]  # 'c' is the last trade price
                prices[pair] = float(last_trade_price)
            else:
                prices[pair] = None  # Handle cases where data is unavailable

        return prices

    def buy(self, asset, amount):
        """Buy the asset with the given amount."""
        asset = Kraken.replace_code(asset)
        pair = asset + "USD"
        print(f"Sending buy order for {amount} of {pair} on Kraken.")
        res = self.api.query_private("AddOrder", {
            "pair": pair,
            "type": "buy",
            "ordertype": "market",
            "volume": amount
        })
        print(res)
        print(f"Placed buy order for {amount} of {asset} on Kraken.")

    def sell(self, asset, amount):
        """Sell the asset with the given amount."""
        asset = Kraken.replace_code(asset)
        res = pair = asset + "USD"
        print(f"Sending sell order for {amount} of {pair} on Kraken.")
        self.api.query_private("AddOrder", {
            "pair": pair,
            "type": "sell",
            "ordertype": "market",
            "volume": amount
        })
        print(res)
        print(f"Placed sell order for {amount} of {asset} on Kraken.")

    @staticmethod
    def replace_code(asset, flag = False):
        # to handle kraken code inconsistency
        code_names = { "XXBT": "XBT", "XETH": "ETH", "XLTC": "LTC",  
            "XXDG": "XDG", "XXMR": "XMR", "XXRP": "XRP", "ZUSD": "USDT",
            "XREP": "XREPZ", "XXLM": "XXLMZ", "XZEC": "XZECZ" }
        if flag: 
            idiotic_codes = {"XXLMZ": "XXLM", "XZECZ": "XZEC", "XREPZ": "XREP"}
            code_names = {**code_names, **idiotic_codes}
        return code_names.get(asset, asset)