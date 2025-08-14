from datetime import datetime

def get_time():
    # Get the current time
    now = datetime.now()

    # Format the time as yyyy-dd-mm H:i:s
    formatted_time = now.strftime("%Y-%d-%m %H:%M:%S")
    return formatted_time

def parse_command(command):
    """Parse a command string into components"""
    command_parts = command.split()
    
    action = command_parts[0]  # The first part will always be the action (e.g., 'buy', 'sell', 'balance')
    
    # If action is 'balance', the second part will always be a string (the target).
    if action == 'balance':
        percent = None
        target = command_parts[1] if len(command_parts) > 1 else 'all'
    else:
        # For other actions, try to parse the percentage (if present)
        percent = float(command_parts[1]) if len(command_parts) > 1 and command_parts[1].replace('.', '', 1).isdigit() else None
        target = command_parts[2] if len(command_parts) > 2 else 'all'

    return action, percent, target


def filter_assets(balance_data, skip_assets, skip_small_asset_value):
    """Filter out the small assets and the ones in skip_assets"""
    filtered_assets = {}
    for asset, amount in balance_data.items():
        if asset in skip_assets or amount < skip_small_asset_value:
            continue
        filtered_assets[asset] = amount
    return filtered_assets

def calculate_changes(balance_data, percent, action):
    """Calculate the new asset amounts based on buy or sell actions"""
    changes = {}
    for asset, amount in balance_data.items():
        change_amount = (amount * percent) / 100
        if action == 'buy':
            changes[asset] = amount + change_amount
        elif action == 'sell':
            changes[asset] = amount - change_amount
    return changes

def get_asset_usd_value(asset, amount, prices, exchange, stable_fiat = "USDT"):
    """Get the USD value of an asset using its price in USDT."""
    # Ensure the asset price is retrieved with the correct symbol (e.g., BTCUSDT)
    if not amount: 
        return 0
    if(exchange.exchange_name == 'kraken'):
        asset = exchange.replace_code(asset)
    
    if(exchange.exchange_name == 'bitfinex'):
        stable_fiat = "USD"
        asset = "t"+asset
    if(exchange.exchange_name == 'coinbase'):
        stable_fiat = "-USD"

    if asset == "USDT" or asset == "tUSD" or asset == "USD" or asset == "USDC":
        return amount * 1
    
    symbol = asset + stable_fiat  # Assuming all assets are paired with USDT for USD conversion
    if symbol in prices:
        price = prices[symbol]
        return amount * price
    else:
        # Handle case when the price is not found
        if(exchange.exchange_name == 'kraken' and stable_fiat == "USDT"):
            return get_asset_usd_value(asset, amount, prices, exchange, "USD")
        
        print(f"Warning: Price for {asset} (symbol {symbol}) not found.")
        return 0


def sort_assets_by_value(assets):
    """Sort the assets by USD/USDT value in descending order"""
    return sorted(assets, key=lambda x: x[2], reverse=True)

def amount_trade(asset, amount, percent):
    decimal = 0
    if amount >= 1 and amount < 10: decimal = 1
    if amount < 1: decimal = 2
    if asset in ["BTC", "ETH", "XBT", "XXBT", "XETH"]: decimal = 3
    if percent < 10: decimal = decimal+1

    return round(amount * (percent / 100), decimal)