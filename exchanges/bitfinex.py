import os
import asyncio
from bfxapi import Client
from .exchange_base import ExchangeBase
from dotenv import load_dotenv

class Bitfinex(ExchangeBase):
    def __init__(self, account_name, exchange_name, api_key, api_secret):
        super().__init__(account_name, exchange_name)
        # Initialize the Bitfinex Client
        self.client = Client(
            api_key=api_key,
            api_secret=api_secret
        )

    def get_balance(self):
        """Get the balance of assets from the Bitfinex account."""
        try:
            # Use authenticated request to fetch wallet balances
            response = self.client.rest.auth.get_wallets()
            return {
                wallet.currency: float(wallet.balance)
                for wallet in response if float(wallet.balance) > 0
            }
        except Exception as e:
            print(f"Error fetching balances: {e}")
            return {}

    def get_prices(self):
        """Get the prices of all assets on Bitfinex."""
        try:
            # List of asset pairs we want to get prices for
            symbols = [
                'tBTCUSD', 'tETHUSD', 'tLTCUSD', 'tXRPUSD', 'tBCHUSD', 'tEOSUSD',
                'tADAUSD', 'tTRXUSD', 'tDOTUSD', 'tUNIUSD', 'tSOLUSD', 'tIOTUSD', 'tBCHNUSD','tBCHUSD','BCHNUSD','BCHUSD', 'tXLMUSD'
            ]

            # Fetch tickers for the specified pairs
            tickers = self.client.rest.public.get_tickers(symbols)
            #print(tickers)
            # Return a dictionary of symbol: last_price
            p = {
                symbol: float(ticker.last_price)  # Access 'last_price' from the 'TradingPairTicker' object
                for symbol, ticker in tickers.items()  # Iterate through tickers dictionary
            }
            #print(p)
            return p

        except Exception as e:
            print(f"Error fetching prices: {e}")
            return {}

    def buy(self, asset, amount):
        """Buy the asset with the given amount."""
        try:
            symbol = f"t{asset.upper()}USD"  # Example: 'tBTCUSD'
            # Place a buy order
            print(f"Sending buy order for {amount} of {symbol} on Bitfinex.")
            self.client.rest.auth.submit_order(symbol, 'buy', 'EXCHANGE MARKET', amount)
            print(f"Placed buy order for {amount} of {asset} on Bitfinex.")
        except Exception as e:
            print(f"Error placing buy order: {e}")

    def sell(self, asset, amount):
        """Sell the asset with the given amount."""
        try:
            symbol = f"t{asset.upper()}USD"  # Example: 'tBTCUSD'
            # Place a sell order
            print(f"Sending sell order for {amount} of {symbol} on Bitfinex.")
            self.client.rest.auth.submit_order(symbol, 'sell', 'EXCHANGE MARKET', amount)
            print(f"Placed sell order for {amount} of {asset} on Bitfinex.")
        except Exception as e:
            print(f"Error placing sell order: {e}")

    def get_margin_balance(self):
        """Get the margin balance of the Bitfinex account."""
        try:
            # Pass the coroutine itself to asyncio.run() without invoking it
            margin_info = self.client.rest.auth.get_base_margin_info()
            margin_balances = {
                'margin_balance': margin_info.margin_balance,
                'margin_net': margin_info.margin_net,
                'margin_min': margin_info.margin_min,
                'user_pl': margin_info.user_pl,
                'user_swaps': margin_info.user_swaps
            }
            #print("🔍 Debug - Margin Info:", margin_balances)
            return margin_balances
        except Exception as e:
            print(f"❌ Error fetching margin balance: {e}")
            return {}

    def get_active_margin_loans(self):
        """Fetch active margin loans with detailed information."""
        try:
            positions = self.client.rest.auth.get_positions()
            active_loans_list = []
            for pos in positions:
                if pos.amount > 0:
                    loan_info = {
                        'symbol': pos.symbol.strip('t'),  # Removing 't' prefix for consistency
                        'amount': float(pos.amount),
                        'base_price': float(pos.base_price),
                        'margin_funding': float(pos.margin_funding),
                        'pl': float(pos.pl),
                        'pl_perc': float(pos.pl_perc),
                        'price_liq': float(pos.price_liq),
                        'leverage': float(pos.leverage)
                    }
                    active_loans_list.append(loan_info)
            #print("🔍 Debug - Active Margin Loans:", active_loans_list)
            return active_loans_list
        except Exception as e:
            print(f"❌ Error fetching active margin loans: {e}")
            return []