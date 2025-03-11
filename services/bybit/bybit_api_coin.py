import time
import requests
from datetime import datetime, timezone, timedelta
import services.data_store
from config import BYBIT_API_URL

def poll_bybit_open_interest():
    while True:
        try:
            symbol = "BTCUSD"
            category = "inverse"
            interval = "5min"
            limit = 1
            end_time = int(time.time() * 1000)
            start_time = end_time - (24 * 60 * 60 * 1000)

            params = {
                "category": category,
                "symbol": symbol,
                "intervalTime": interval,
                "limit": limit,
                "startTime": start_time,
                "endTime": end_time
            }

            response = requests.get(BYBIT_API_URL, params=params)
            data = response.json()

            if response.status_code != 200 or "result" not in data:
                print(f"Error fetching Bybit Open Interest: {response.status_code}, {response.text}")
                continue

            data_list = data["result"]["list"]
            if not data_list:
                print("Error: 'list' is empty in Bybit API response")
                continue

            latest_data = data_list[0]  # 取最新的一条数据
            open_interest = round(float(latest_data["openInterest"]), 2)
            total_value_billion = round(open_interest / 1_0000_0000, 2)  # 转换为 亿 USDT，保留两位小数

            dt_object = datetime.fromtimestamp(int(latest_data["timestamp"]) / 1000, tz=timezone.utc) + timedelta(hours=8)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

            services.data_store.update_market_data("bybit", "btc", "coin", "open_interest", total_value_billion, formatted_time)

        except Exception as e:
            print(f"Error fetching Bybit Open Interest: {e}")

        time.sleep(1)