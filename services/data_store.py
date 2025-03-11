import json


market_data = {
    "okx": {},
    "binance": {},
    "bybit": {}
}

def update_market_data(exchange, coin, contract_type, data_type, value, timestamp):

    if exchange not in market_data:
        market_data[exchange] = {}

    if coin not in market_data[exchange]:
        market_data[exchange][coin] = {}

    if contract_type not in market_data[exchange][coin]:
        market_data[exchange][coin][contract_type] = {}

    market_data[exchange][coin][contract_type][data_type] = {
        "value": value,
        "time": timestamp
    }

def get_market_data():
    return market_data

# **示例更新**
# update_market_data("okx", "btc", "usdt", "funding_rate", 0, 0)
# update_market_data("okx", "btc", "usdt", "open_interest", 0, 0)
# update_market_data("okx", "btc", "coin", "funding_rate", 0, 0)
# update_market_data("okx", "btc", "usdc", "funding_rate", 0, 0)
# print(json.dumps(market_data, indent=4))