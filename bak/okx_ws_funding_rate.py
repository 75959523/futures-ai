import asyncio
import websockets
import json
from datetime import datetime, timezone, timedelta

OKX_WS_URL = "wss://ws.okx.com:8443/ws/v5/public"

async def subscribe_funding_rate():
    async with websockets.connect(OKX_WS_URL) as ws:
        # 发送订阅请求
        subscribe_message = {
            "op": "subscribe",
            "args": [
                {
                    "channel": "funding-rate",
                    "instId": "BTC-USD-SWAP"
                }
            ]
        }
        await ws.send(json.dumps(subscribe_message))
        # print("已发送订阅请求:", json.dumps(subscribe_message, indent=4, ensure_ascii=False))

        # 监听推送数据
        while True:
            response = await ws.recv()
            data = json.loads(response)
            # print("收到数据:", json.dumps(data, indent=4, ensure_ascii=False))

            if "data" in data:
                for entry in data["data"]:
                    for key, value in entry.items():
                        if key == "fundingRate":
                            funding_rate_percentage = float(value) * 100
                            formatted_funding_rate = f"{funding_rate_percentage:.6f}%"
                            print(f"okx : {formatted_funding_rate}")
                        elif key == "ts":
                            dt_object = datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc) + timedelta(hours=8)
                            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                            print(f"{formatted_time}")

asyncio.run(subscribe_funding_rate())