import time
import requests
from datetime import datetime, timezone, timedelta
from config import BINANCE_API_URL_COIN
import services.data_store

def poll_binance_open_interest():
    while True:
        try:
            response = requests.get(BINANCE_API_URL_COIN)
            data = response.json()

            if "openInterest" not in data:
                print("Error: 'openInterest' key not found in Binance API response")
                continue

            open_interest = float(data["openInterest"])  # 获取未平仓合约量（张）
            total_value = open_interest * 100  # 计算未平仓总金额（USDT）
            total_value_billion = round(total_value / 1_0000_0000, 2)  # 转换为 亿 USDT，保留两位小数

            dt_object = datetime.fromtimestamp(data["time"] / 1000, tz=timezone.utc) + timedelta(hours=8)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

            services.data_store.update_market_data("binance", "btc", "coin", "open_interest", total_value_billion, formatted_time)

        except Exception as e:
            print(f"Error fetching Binance Open Interest: {e}")

        time.sleep(1)  # 每隔 1 秒轮询一次