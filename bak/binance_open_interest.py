import requests
import time
import datetime
from datetime import datetime, timezone, timedelta
from config import BINANCE_API_URL_COIN


def get_open_interest():
    try:
        response = requests.get(BINANCE_API_URL_COIN)
        data = response.json()

        # 确保 API 返回的数据包含 `openInterest`
        if "openInterest" not in data:
            print("Error: 'openInterest' key not found in API response")
            return

        dt_object = datetime.fromtimestamp(data["time"]  / 1000, tz=timezone.utc) + timedelta(hours=8)
        formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

        open_interest = float(data["openInterest"])

        print(f"binance : Open Interest: {open_interest:.2f}  {formatted_time}")

    except Exception as e:
        print(f"Error fetching Binance Open Interest: {e}")

if __name__ == "__main__":
    while True:
        get_open_interest()
        time.sleep(1)