import time
import requests
from datetime import datetime, timezone, timedelta
from config import BINANCE_API_URL
import services.data_store

def poll_binance_open_interest():

    while True:
        try:
            response = requests.get(BINANCE_API_URL)
            data = response.json()

            if "openInterest" not in data:
                print("Error: 'openInterest' key not found in Binance API response")
                continue

            dt_object = datetime.fromtimestamp(data["time"] / 1000, tz=timezone.utc) + timedelta(hours=8)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

            # 更新全局变量
            services.data_store.binance_open_interest = {
                "open_interest": round(float(data["openInterest"]), 2),
                "timestamp": formatted_time
            }

        except Exception as e:
            print(f"Error fetching Binance Open Interest: {e}")

        time.sleep(1)  # 每隔 1 秒轮询一次