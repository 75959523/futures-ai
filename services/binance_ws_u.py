import json
import websocket
import time
from datetime import datetime, timezone, timedelta
from config import BINANCE_WS_URL_U
import services.data_store

def on_binance_message(ws, message):
    """ 处理 Binance WebSocket 消息 """
    data = json.loads(message)

    if data.get("e") == "markPriceUpdate":
        dt_object = datetime.fromtimestamp(data["E"] / 1000, tz=timezone.utc) + timedelta(hours=8)
        formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

        mark_price_str = data.get("p")
        funding_rate_str = data.get("r")

        if mark_price_str is None or funding_rate_str is None:
            print(f"Warning: Binance received None values. Data: {data}")
            return

        try:
            mark_price = float(mark_price_str)
            funding_rate = float(funding_rate_str) * 100
        except ValueError:
            print(f"ValueError: Binance invalid numeric values. Data: {data}")
            return

        services.data_store.update_market_data("binance", "btc", "u", "mark_price",
                                               round(mark_price, 2), formatted_time)
        services.data_store.update_market_data("binance", "btc", "u", "funding_rate",
                                               f"{funding_rate:.6f}%", formatted_time)

def on_binance_error(ws, error):
    print(f"Binance WebSocket Error: {error}")

def on_binance_close(ws, close_status_code, close_msg):
    print("### Binance WebSocket Closed ###")

def on_binance_open(ws):
    payload = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@markPrice@1s"],
        "id": 1
    }
    ws.send(json.dumps(payload))
    # print("Binance Subscribed to funding rate")

def start_binance_ws():
    """ Binance WebSocket 运行函数，独立启动 """
    while True:
        try:
            ws = websocket.WebSocketApp(BINANCE_WS_URL_U,
                on_message=on_binance_message,
                on_error=on_binance_error,
                on_close=on_binance_close
            )
            ws.on_open = on_binance_open
            ws.run_forever()
        except Exception as e:
            print(f"Binance WebSocket connection error: {e}")
            time.sleep(5)