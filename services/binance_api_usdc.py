import time
import requests
from datetime import datetime, timezone, timedelta
from config import BINANCE_API_URL_USDC
import services.data_store

def poll_binance_open_interest():

    while True:
        try:
            response = requests.get(BINANCE_API_URL_USDC)
            data = response.json()

            if "openInterest" not in data:
                print("Error: 'openInterest' key not found in Binance API response")
                continue

            dt_object = datetime.fromtimestamp(data["time"] / 1000, tz=timezone.utc) + timedelta(hours=8)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

            services.data_store.update_market_data("binance", "btc", "usdc", "open_interest", round(float(data["openInterest"]), 2), formatted_time)

        except Exception as e:
            print(f"Error fetching Binance Open Interest: {e}")

        time.sleep(1)  # 每隔 1 秒轮询一次