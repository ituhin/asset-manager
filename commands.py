from utils import get_time, amount_trade, parse_command, filter_assets, calculate_changes, get_asset_usd_value, sort_assets_by_value
from exchanges import get_exchange
from logger import get_logger
from config import load_config


logger = get_logger()

# Caching balances in memory
exchange_balances = {}

def execute_command(command):
    """Parse and execute the commands"""
    print(get_time())
    # Load config
    config = load_config()
    
    action, percent, target = parse_command(command)
    
    if action == 'balance':
        show_balance(target, config)
    elif action in ['buy', 'sell']:
        if percent and target:
            perform_trade(action, percent, target, config)
    elif action == 'margin':
        handle_margin(config)
    else:
        print("Invalid command!")

def perform_trade(action, percent, target, config):
    """
    Handle buy or sell action across specified exchanges and accounts.
    """
    # Parse the target to determine the exchange and account
    if target == 'all':
        target_exchange, target_account = None, None
    else:
        target_exchange, target_account = target.split('_')

    exchanges = config['accounts']
    for exchange_name, accounts in exchanges.items():
        # Skip if the exchange doesn't match the target
        if target_exchange and exchange_name != target_exchange:
            continue

        for account_name in accounts:
            # Skip if the account doesn't match the target
            if target_account and account_name != target_account:
                continue

            # Delegate the trade operation to perform_trade_for_account
            perform_trade_for_account(action, percent, exchange_name, account_name, config)

def handle_margin(config):
    """Handle margin-related commands"""
    accounts = config.get('accounts', {})
    
    for exchange_name, account_names in accounts.items():
        for account_name in account_names:
            try:
                exchange = get_exchange(exchange_name, account_name)
                
                if hasattr(exchange, 'get_margin_balance'):
                    margin_balance = exchange.get_margin_balance()
                    if exchange_name == 'bitfinex':
                        display_margin_balances_bitfinex(account_name, exchange.exchange_name, margin_balance)
                    else:
                        display_margin_balances(account_name, exchange.exchange_name, margin_balance)
                
                # Fetch and display active margin loans
                if hasattr(exchange, 'get_active_margin_loans'):
                    active_loans = exchange.get_active_margin_loans()
                    if exchange_name == 'bitfinex':
                        display_active_loans_bitfinex(account_name, exchange.exchange_name, active_loans)
                    else:
                        display_active_loans(account_name, exchange.exchange_name, active_loans)
                
            except Exception as e:
                print(f"❌ Error handling margin for {account_name} on {exchange_name}: {e}")

def perform_trade_for_account(action, percent, exchange_name, account_name, config):
    """
    Perform buy or sell operations for a specific exchange and account.
    """
    # Prepare balance data for the specified account
    sorted_assets, _ = prepare_balance_for_account(exchange_name, account_name, config)

    # Filter out assets listed in the skip_assets configuration
    skip_assets = config.get("skip_assets", [])
    filtered_assets = [
        asset_data for asset_data in sorted_assets if asset_data[0] not in skip_assets
    ]

    for asset, amount, usd_value, _, _ in filtered_assets:
        # Calculate the amount to trade
        amount_to_trade = amount_trade(asset, amount, percent)

        # Get exchange instance
        exchange = get_exchange(exchange_name, account_name)
        
        # Log the action if live flag is True
        if config['live']:
            # Perform the buy/sell operation using exchange's API
            if action == 'buy':
                exchange.buy(asset, amount_to_trade)
            elif action == 'sell':
                exchange.sell(asset, amount_to_trade)
            logger.info(f"{action.capitalize()} {amount_to_trade} of {asset} on {exchange_name}_{account_name}")
        else:
            print(f"[Simulation] {action.capitalize()} {amount_to_trade} of {asset} on {exchange_name}_{account_name}")


def get_balance(exchange_name, account_name, exchange):
    """Get balance data, either from cache or by fetching it from the exchange"""
    if f"{exchange_name}_{account_name}" not in exchange_balances:
        print(f"Fetching balance for {exchange_name}_{account_name}...")
        balance_data = exchange.get_balance()
        exchange_balances[f"{exchange_name}_{account_name}"] = balance_data
    return exchange_balances[f"{exchange_name}_{account_name}"]

def filter_balance(balance_data, prices, config, exchange):
    """Filter balance data by adding USD value and applying filters like skip_assets and skip_small_asset_usd"""
    filtered_balance_with_usd = {}
    for asset, amount in balance_data.items():
        usd_value = get_asset_usd_value(asset, amount, prices, exchange)
        if usd_value and usd_value >= config.get('skip_small_asset_usd', 0):
            filtered_balance_with_usd[asset] = usd_value
    return filter_assets(filtered_balance_with_usd, [], config.get('skip_small_asset_usd', 0))

def prepare_balance_for_account(exchange_name, account_name, config):
    """Prepare balance data for a specific account"""
    exchange = get_exchange(exchange_name, account_name)
    balance_data = get_balance(exchange_name, account_name, exchange)
    prices = exchange.get_prices()

    filtered_balance = filter_balance(balance_data, prices, config, exchange)

    asset_list = []
    for asset, usd_value in filtered_balance.items():
        amount = balance_data.get(asset, 0)
        asset_list.append((asset, amount, usd_value, exchange_name, account_name))

    sorted_assets = sort_assets_by_value(asset_list)
    total_value = sum(usd_value for _, _, usd_value, _, _ in sorted_assets)

    return sorted_assets, total_value

def print_balance_for_account(sorted_assets, total_value, exchange_name, account_name=None):
    """Print the balance data for a specific account"""
    for asset, amount, usd_value, exchange, account in sorted_assets:
        print(f"{asset:<20}{amount:<15}{usd_value:<15.2f}{exchange}_{account}")
    if account_name:
        print("-" * 60)
        print(f"{'Total Value for Account':<50}{total_value:<15.2f}")
        print(" " * 60)
    else:
        print(f"{'Total Value for Exchange':<50}{total_value:<15.2f}")

def show_balance(target, config):
    """Display balances from exchanges"""
    if target == 'all':
        for exchange_name, accounts in config['accounts'].items():
            total_exchange_value = 0
            print(f"\nBalance for Exchange: {exchange_name}")
            print("=" * 60)
            for account_name in accounts:
                sorted_assets, account_total_value = prepare_balance_for_account(exchange_name, account_name, config)
                print_balance_for_account(sorted_assets, account_total_value, exchange_name, account_name)
                total_exchange_value += account_total_value

            print("=" * 60)
            print(f"{'Total Value for Exchange':<50}{total_exchange_value:<15.2f}")
    else:
        exchange_name, account_name = target.split('_')
        sorted_assets, account_total_value = prepare_balance_for_account(exchange_name, account_name, config)
        print_balance_for_account(sorted_assets, account_total_value, exchange_name, account_name)

# utils.py


def display_margin_balances(account_name, exchange_name, margin_balances):
    """Display margin balances for a given account and exchange."""
    if not margin_balances:
        print(f"No margin balances found for {account_name} on {exchange_name}.")
        return
    
    print(f"\nMargin Balances for {account_name} on {exchange_name}:")
    print("-" * 60)
    print(f"{'Asset':<10}{'Free':<20}{'Borrowed':<20}{'Total':<10}")
    print("-" * 60)
    for asset, balances in margin_balances.items():
        print(f"{asset:<10}{balances.get('free', 0):<20}{balances.get('borrowed', 0):<20}{balances.get('total', 0):<10}")
    print("-" * 60)


def display_active_loans(account_name, exchange_name, active_loans):
    """Display active margin loans for a given account and exchange."""
    if not active_loans:
        print(f"ℹ️ No active margin loans found for {account_name} on {exchange_name}.")
        return
    
    print(f"\nActive Margin Loans for {account_name} on {exchange_name}:")
    print("-" * 60)
    print(f"{'Asset':<10}{'Borrowed':<20}")
    print("-" * 60)
    for asset, borrowed in active_loans.items():
        print(f"{asset:<10}{borrowed:<20}")
    print("-" * 60)

# utils.py


def display_margin_balances_bitfinex(account_name, exchange_name, margin_balances):
    """Display margin balances for a given account and exchange."""
    if not margin_balances:
        print(f"No margin balances found for {account_name} on {exchange_name}.")
        return

    print(f"\nMargin Balances for {account_name} on {exchange_name}:")
    print("-" * 60)
    print(f"{'Margin Balance':<20}{margin_balances.get('margin_balance', 0):<20}")
    print(f"{'Margin Net':<20}{margin_balances.get('margin_net', 0):<20}")
    print(f"{'Margin Min':<20}{margin_balances.get('margin_min', 0):<20}")
    print(f"{'User P&L':<20}{margin_balances.get('user_pl', 0):<20}")
    print(f"{'User Swaps':<20}{margin_balances.get('user_swaps', 0):<20}")
    print("-" * 60)


def display_active_loans_bitfinex(account_name, exchange_name, active_loans):
    """Display active margin loans for a given account and exchange."""
    if not active_loans:
        print(f"ℹ️ No active margin loans found for {account_name} on {exchange_name}.")
        return

    print(f"\nActive Margin Loans for {account_name} on {exchange_name}:")
    print("-" * 100)
    print(f"{'Symbol':<10}{'Amount':<10}{'Base Price':<15}{'Margin Funding':<15}{'P&L':<10}{'P&L%':<10}{'Price LIQ':<10}{'Leverage':<10}")
    print("-" * 100)
    for loan in active_loans:
        print(f"{loan.get('symbol', ''):<10}{loan.get('amount', 0):<10.4f}{loan.get('base_price', 0):<15.4f}"
              f"{loan.get('margin_funding', 0):<15.4f}{loan.get('pl', 0):<10.2f}"
              f"{loan.get('pl_perc', 0):<10.2f}{loan.get('price_liq', 0):<10.2f}"
              f"{loan.get('leverage', 0):<10.4f}")
    print("-" * 100)