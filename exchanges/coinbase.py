from coinbase.rest import RESTClient
from .exchange_base import ExchangeBase

class Coinbase(ExchangeBase):
    def __init__(self, account_name, exchange_name, api_key, api_secret):
        super().__init__(account_name, exchange_name)

        self.client = RESTClient(api_key, api_secret)

    def get_balance(self):
        """Get the balance of assets from the Coinbase account."""
        try:
            accounts = self.client.get_accounts()
            balances = {}
            for account in accounts['accounts']:
                currency = account['currency']
                amount = float(account['available_balance']['value'])
                balances[currency] = amount
            return balances
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return {}

    def get_prices(self):
        """Get the spot prices of all currency pairs."""
        try:
            products = self.client.get_products()
            #print(products)
            prices = {}
            for product in products['products']:
                if product['price']:
                    prices[product['product_id']] = float(product['price'])

            return prices
        except Exception as e:
            print(f"Error fetching prices: {e}")
            return {}

    def buy(self, asset, amount):
        """Buy the asset with the given amount using a market order."""
        try:
            product_id = f"{asset}-USD"
            print(f"Sending buy order for {amount} of {product_id} on Coinbase.")
            response = self.client.market_order_buy(client_order_id="", product_id=product_id, base_size=str(amount))
            print(f"Buy order placed: {response}")
            return response
        except Exception as e:
            print(f"Error placing buy order: {e}")
            return {}

    def sell(self, asset, amount):
        """Sell the asset with the given amount using a market order."""
        try:
            product_id = f"{asset}-USD"
            print(f"Sending sell order for {amount} of {product_id} on Coinbase.")
            response = self.client.market_order_sell(client_order_id="", product_id=product_id, base_size=str(amount))
            print(f"Sell order placed: {response}")
            return response
        except Exception as e:
            print(f"Error placing sell order: {e}")
            return {}