import asyncio
import websockets
import json
from datetime import datetime, timezone, timedelta
from config import BYBIT_WS_URL_U
import services.data_store

async def subscribe_bybit_funding_rate(symbol="BTCUSDT"):
    topic = f"tickers.{symbol}"

    while True:
        try:
            async with websockets.connect(BYBIT_WS_URL_U, ping_interval=30) as ws:
                subscribe_msg = {"op": "subscribe", "args": [topic]}
                await ws.send(json.dumps(subscribe_msg))

                while True:
                    try:
                        response = await asyncio.wait_for(ws.recv(), timeout=10)
                        data = json.loads(response)
                        if "data" not in data:
                            continue
                        ticker_data = data["data"]
                        if "fundingRate" in ticker_data and ticker_data["fundingRate"] is not None:
                            funding_rate = float(ticker_data["fundingRate"]) * 100
                            dt_object = datetime.now(timezone.utc) + timedelta(hours=8)
                            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

                            services.data_store.update_market_data("bybit", "btc", "u", "funding_rate", f"{funding_rate:.6f}%", formatted_time)

                        if "markPrice" in ticker_data and ticker_data["markPrice"] is not None:
                            mark_price = round(float(ticker_data["markPrice"]), 2)
                            dt_object = datetime.now(timezone.utc) + timedelta(hours=8)
                            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

                            services.data_store.update_market_data("bybit", "btc", "u", "mark_price", mark_price, formatted_time)

                    except asyncio.TimeoutError:
                        print("Bybit Timeout waiting for response, retrying...")
        except Exception as e:
            print(f"Bybit WebSocket Error: {e}, reconnecting in 5 seconds...")
            await asyncio.sleep(5)