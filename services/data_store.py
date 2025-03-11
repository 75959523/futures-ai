
market_data = {
    "okx": {},
    "binance": {},
    "bybit": {}
}

def update_market_data(exchange: str, coin: str, contract_type: str, data_type: str, value, timestamp):
    """
    更新市场数据
    :param exchange: 交易所名称 (okx, binance, bybit)
    :param coin: 币种 (btc, eth, sol, etc.)
    :param contract_type: 合约类型 (u, coin, usdc)
    :param data_type: 数据类型 (mark_price, open_interest, funding_rate)
    :param value: 数据值
    :param timestamp: 时间戳 (格式 "YYYY-MM-DD HH:MM:SS")
    """
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