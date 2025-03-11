import requests
import datetime
import time
from datetime import datetime, timezone, timedelta

BYBIT_API_URL = "https://api.bybit.com/v5/market/open-interest"


def get_latest_open_interest(symbol="BTCUSD", category="inverse", interval="5min", limit=1):
    end_time = int(time.time() * 1000)  # 当前时间（毫秒）
    start_time = end_time - (24 * 60 * 60 * 1000)  # 24 小时前的时间戳

    params = {
        "category": category,
        "symbol": symbol,
        "intervalTime": interval,
        "limit": limit,
        "startTime": start_time,
        "endTime": end_time
    }

    response = requests.get(BYBIT_API_URL, params=params)
    if response.status_code == 200 and "result" in response.json():
        data = response.json()["result"]["list"]
        if data:
            latest_data = data[0]  # 只取最新一条数据
            open_interest = round(float(latest_data["openInterest"]), 2)

            dt_object = datetime.fromtimestamp(int(latest_data["timestamp"])/ 1000, tz=timezone.utc) + timedelta(hours=8)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            return formatted_time, open_interest

    print(f"Error: {response.status_code}, {response.text}")
    return None, None


def main():
    try:
        while True:
            latest_time, latest_oi = get_latest_open_interest()
            if latest_time and latest_oi is not None:
                print(f"bybit : {latest_oi} {latest_time}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    main()