import time
import requests
from datetime import datetime, timezone, timedelta
import services.data_store
from config import BYBIT_API_URL

def poll_bybit_open_interest():
    while True:
        try:
            symbol = "BTCUSDT"
            category = "linear"
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

            dt_object = datetime.fromtimestamp(int(latest_data["timestamp"]) / 1000, tz=timezone.utc) + timedelta(hours=8)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

            # 更新全局数据
            services.data_store.bybit_open_interest = {
                "open_interest": open_interest,
                "timestamp": formatted_time
            }

        except Exception as e:
            print(f"Error fetching Bybit Open Interest: {e}")

        time.sleep(1)