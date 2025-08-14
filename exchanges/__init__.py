# exchanges/__init__.py
import os
from .binance import Binance
from .kraken import Kraken
from .bitfinex import Bitfinex
from .coinbase import Coinbase
#from .bitget import Bitget
#from .kucoin import KuCoin
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

def get_api_keys(exchange_name, account_name):
    """ Load the API key and secret from the .env file based on exchange and account name """
    api_key = os.getenv(f"{exchange_name.upper()}_{account_name.upper()}_API_KEY")
    api_secret = os.getenv(f"{exchange_name.upper()}_{account_name.upper()}_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError(f"API keys for {account_name} on {exchange_name} not found in .env")
    
    # For KuCoin, we also need to load passphrase
    if exchange_name.lower() == 'kucoin':
        api_passphrase = os.getenv(f"{exchange_name.upper()}_{account_name.upper()}_API_PASSPHRASE")
        if not api_passphrase:
            raise ValueError(f"API passphrase for {account_name} on {exchange_name} not found in .env")
        return api_key, api_secret, api_passphrase
    return api_key, api_secret

def get_exchange(exchange_name, account_name):
    """ Get an instance of the exchange class based on the exchange name and account name """
    if exchange_name.lower() == 'binance':
        api_key, api_secret = get_api_keys(exchange_name, account_name)
        return Binance(account_name, exchange_name, api_key, api_secret)
    elif exchange_name.lower() == 'kraken':
        api_key, api_secret = get_api_keys(exchange_name, account_name)
        return Kraken(account_name, exchange_name, api_key, api_secret)
    elif exchange_name.lower() == 'bitfinex':
        api_key, api_secret = get_api_keys(exchange_name, account_name)
        return Bitfinex(account_name, exchange_name, api_key, api_secret)
    elif exchange_name.lower() == 'coinbase':
        api_key, api_secret = get_api_keys(exchange_name, account_name)
        return Coinbase(account_name, exchange_name, api_key, api_secret)
    elif exchange_name.lower() == 'bitget':
        api_key, api_secret = get_api_keys(exchange_name, account_name)
        return Bitget(account_name, exchange_name, api_key, api_secret)
    elif exchange_name.lower() == 'kucoin':
        api_key, api_secret, api_passphrase = get_api_keys(exchange_name, account_name)
        return KuCoin(account_name, exchange_name, api_key, api_secret, api_passphrase)
    else:
        raise ValueError(f"Exchange {exchange_name} is not supported.")
