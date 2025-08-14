# exchanges/binance.py
import os
from binance.client import Client
from .exchange_base import ExchangeBase
from dotenv import load_dotenv

load_dotenv()

class Binance(ExchangeBase):
    fiat = "USDC"
    
    def __init__(self, account_name, exchange_name, api_key, api_secret):
        super().__init__(account_name, exchange_name)

        if os.getenv('EXCHANGE_SANDBOX', 'false').lower() == 'true':
            self.client = Client(api_key, api_secret, testnet=True)
        else: 
            self.client = Client(api_key, api_secret)
        

    def get_balance(self):
        """Get the balance of assets from the Binance account."""
        balance_data = self.client.get_account()["balances"]
        return {balance["asset"]: float(balance["free"]) for balance in balance_data if float(balance["free"]) > 0}

    def get_prices(self):
        """Get the prices of assets on Binance."""
        prices = self.client.get_all_tickers()
        return {price["symbol"]: float(price["price"]) for price in prices}

    def buy(self, asset, amount):
        """Buy the asset with the given amount."""
        symbol = asset + self.fiat
        print(f"Sending buy order for {amount} of {asset} on Binance.")
        res = self.client.order_market_buy(symbol=symbol, quantity=amount)
        print(res)
        print(f"Placed buy order for {amount} of {asset} on Binance.")

    def sell(self, asset, amount):
        """Sell the asset with the given amount."""
        symbol = asset + self.fiat
        print(f"Sending sell order for {amount} of {asset} on Binance.")
        res = self.client.order_market_sell(symbol=symbol, quantity=amount)
        print(res)
        print(f"Placed sell order for {amount} of {asset} on Binance.")
    
    def get_margin_balance(self):
        """Get the margin balance of the Binance account."""
        try:
            margin_info = self.client.get_margin_account()
            #print("🔍 Debug - Margin Info:", margin_info)  # Debugging statement

            #p = self.client.papi_get_balance()
            #print("🔍 Debug - PAPI Balance:", p)  # Debugging statement
            #pp = self.client.papi_get_account()
            #print("🔍 Debug - PAPI Acc:", pp)

            if not isinstance(margin_info, dict):
                raise ValueError(f"Unexpected response type: {type(margin_info)}. Response: {margin_info}")

            user_assets = margin_info.get('userAssets', [])

            if not user_assets:
                print("ℹ️ No margin assets found. Ensure margin trading is enabled and there are active margin positions.")

            margin_balances = {
                asset['asset']: {
                    'borrowed': float(asset.get('borrowed', 0)),
                    'free': float(asset.get('free', 0)),
                    'total': float(asset.get('total', 0))
                }
                for asset in user_assets
                if float(asset.get('borrowed', 0)) > 0 or float(asset.get('free', 0)) > 0
            }

            return margin_balances
        except Exception as e:
            print(f"❌ Error fetching margin balance: {e}")
            return {}
    
    def get_active_margin_loans(self):
        """Fetch active margin loans by parsing the margin account."""
        try:
            margin_info = self.client.get_margin_account()
            active_loans = {}
            for asset in margin_info.get('userAssets', []):
                borrowed = float(asset.get('borrowed', 0))
                if borrowed > 0:
                    active_loans[asset['asset']] = borrowed
            #print("🔍 Debug - Active Margin Loans:", active_loans)  # Debugging statement
            return active_loans
        except Exception as e:
            print(f"❌ Error fetching active margin loans: {e}")
            return {}