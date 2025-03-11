import asyncio
import websockets
import json
from datetime import datetime, timezone, timedelta

# **全局变量**
funding_rate = None
mark_price = None
funding_time = None

async def funding_rate_listener(symbol="BTCUSDT"):
    global funding_rate, mark_price, funding_time
    url = "wss://stream.bybit.com/v5/public/linear"
    topic = f"tickers.{symbol}"

    async with websockets.connect(url, ping_interval=30) as ws:
        subscribe_msg = {"op": "subscribe", "args": [topic]}
        await ws.send(json.dumps(subscribe_msg))
        print(f"Subscribed to {topic}")

        async def print_status():
            global funding_time
            while True:
                funding_time1 = funding_time if funding_time else "N/A"
                funding_rate1 = funding_rate if funding_rate else "N/A"

                print(f"Funding Rate: {funding_rate1:.6f}%, Mark Price: {mark_price}, Update Time: {funding_time1}" if isinstance(funding_rate1, float) else f"Funding Rate: {funding_rate1}, Mark Price: {mark_price}, Update Time: {funding_time1}")
                await asyncio.sleep(1)

        asyncio.create_task(print_status())

        while True:
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(response)

                if not isinstance(data, dict):
                    continue

                if data.get("type") == "snapshot" and "data" in data and isinstance(data["data"], dict):
                    ticker_data = data["data"]
                    if "fundingRate" in ticker_data and ticker_data["fundingRate"] is not None:
                        funding_rate = float(ticker_data["fundingRate"]) * 100

                        dt_object = datetime.fromtimestamp(int(ticker_data["nextFundingTime"]) / 1000,tz=timezone.utc) + timedelta(hours=8)
                        funding_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

                    if "markPrice" in ticker_data and ticker_data["markPrice"] is not None:
                        mark_price = round(float(ticker_data["markPrice"]), 2)

            except asyncio.TimeoutError:
                print("Timeout waiting for response, reconnecting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

# 运行 WebSocket 监听
asyncio.run(funding_rate_listener("BTCUSDT"))