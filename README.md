<h2>Crypto asset manager </h2>
to easily manage 100s of assets across many exchanges and accounts pair at once. Useful when you have lot of assets spread across multiple exchanges/accounts and wants to take quick actions or get all status reports from everywhere.

<h5>Can be used as crypto panic button too :)</h5>

## Installation 
python3 required
```
pip install -r requirements.txt
```

## Configure
1. config.json

   ```"live": true,``` if live = false, it do not connect to exchange apis for buy/sell, only prints - simulation


   ```"skip_assets": ["BTC", "USDT", "USDC", "FDUSD", "TUSD", "USD"],``` buy or sell actions wont be applicable on these mentioned assets, mention the fiats you have here, and assets you dont want to touch


   ```"skip_small_asset_usd": 10, ``` in USD, assets which are very small in size wont be touched at all, eg: 10 USD or less in values will be ignored from displaying or buy/sell.


   ```
   "accounts": {
        "binance": ["tuhin", "barua", "monu"],
        "kraken": ["monu"],
        "coinbase": ["monu"],
        "bitfinex": ["tuhin", "barua"]
    }
   ```
   we can add multiple accounts from the same exchange.
   currently it handles binance, kraken, coinbase, bitfinex - other exchanges can be added in the exchange layer.


2. rename .env.example to .env  -- this holds api key and secret

   structure -> ```{EXCHANGE}_{ACCOUNT}_API_KEY || {EXCHANGE}_{ACCOUNT}_API_SECRET``` 

   set it appropriately as per the exchange-account pair configured already in config.json

   eg: ```BINANCE_TUHIN_API_KEY={key from your binance account}```, here TUHIN is account alias so that we can add more accounts from binance exchange

   ```EXCHANGE_SANDBOX=false``` -- if set to true it will try to connect to sandbox api, 

   note: only kraken and binance have sandbox, this param only applicable for these 2 exchanges

## Running the app
```bash
python3 main.py
```

you will get a ```$$$``` prompt which takes commands

## Usage
there are 3 commands currently --> ```balance, buy, sell``` - each actions can target exchange_account pair, in the absense of target default is all

1. ```balance {exchange_account}``` -> eg: "balance coinbase_tuhin" will fetch all assets from the target exchange_account pair and list them down in sorted order by the USD amount, and display total value

2. ```balance or balance all``` -> will fetch all the assets as per the exchanges/accounts pair configured in config, in the same order as config, grouped by exchange_account as displayed above
   
3. ```buy {percent} {exchange_account}``` -> eg: "buy 20 binance_tuhin" -- will try to increase 20% of each existing asset postion, if XRP exists in the account and existing XRP size is 100, it would try to buy 20 more at market order, success or failure of the order depends on the fiat USD/USDC/USDT available in the account.
4. ```buy {percent} all``` -> will be applicable to all the configured exchange_account pairs in config, same like the above command.
5. ```sell {percent} {exchange_account}``` -> eg: "sell 30 binance_tuhin" -- will try to reduce 30% of each existing asset postion, if XRP exists in the account and existing XRP size is 200, it would try to buy 60 more at market order, success or failure of the order depends on the fiat USD available in the account.
6. ```sell {percent} all``` -> eg: sell 90 all -- will reduce 90% of each existing asset positions in all the configured exchange account pair

Note: currently base fiat set as USD in kraken, coinbase, bitfinex, and USDC in binance as base pair, in the respective exchanges file.

## Example

```
💰$$$ balance coinbase_tuhin
2025-15-08 02:40:08
Fetching balance for coinbase_tuhin...
XRP                 4499.839       13834.76       coinbase_tuhin
USD                 1618.50636318  1618.51        coinbase_tuhin
------------------------------------------------------------
Total Value for Account                           15453.26 
```
