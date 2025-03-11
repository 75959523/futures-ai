import json
import websocket
import datetime
import time
from datetime import datetime, timezone, timedelta
from config import BINANCE_WS_URL_COIN

def on_message(ws, message):
    data = json.loads(message)

    if data.get("e") == "markPriceUpdate":
        dt_object = datetime.fromtimestamp(data["E"] / 1000, tz=timezone.utc) + timedelta(hours=8)
        formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

        mark_price_str = data.get("p")
        funding_rate_str = data.get("r")

        # 确保值不为空
        if mark_price_str is None or funding_rate_str is None:
            print(f"Warning: Received None values. Data: {data}")
            return

        try:
            mark_price = float(mark_price_str)
            funding_rate = float(funding_rate_str) * 100
        except ValueError:
            print(f"ValueError: Invalid numeric values received. Data: {data}")
            return

        log_entry = f"binance : Mark Price: {mark_price:.2f} Funding Rate: {funding_rate:.6f}%  {formatted_time} \n"
        print(log_entry, end="")

def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("### Binance WebSocket Closed ###")


def on_open(ws):
    payload = {
        "method": "SUBSCRIBE",
        "params": ["btcusd_perp@markPrice@1s"],
        "id": 1
    }
    ws.send(json.dumps(payload))
    print("Subscribed to Binance funding rate")


def start_binance_ws():
    while True:
        try:
            ws = websocket.WebSocketApp(
                BINANCE_WS_URL_COIN,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.on_open = on_open
            ws.run_forever()
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    start_binance_ws()