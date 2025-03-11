import asyncio
import websockets
import json
from datetime import datetime, timezone, timedelta

OKX_WS_URL = "wss://ws.okx.com:8443/ws/v5/public"


async def subscribe_open_interest():
    async with websockets.connect(OKX_WS_URL) as ws:
        # 发送订阅请求
        subscribe_message = {
            "op": "subscribe",
            "args": [
                {
                    "channel": "open-interest",
                    "instId": "BTC-USDT-SWAP"
                }
            ]
        }
        await ws.send(json.dumps(subscribe_message))
        # print("已发送订阅请求:", json.dumps(subscribe_message, indent=4, ensure_ascii=False))

        # 监听推送数据
        while True:
            response = await ws.recv()
            data = json.loads(response)

            if "data" in data:
                for entry in data["data"]:
                    oi_ccy = float(entry["oiCcy"])
                    ts = int(entry["ts"])

                    dt_object = datetime.fromtimestamp(ts / 1000, tz=timezone.utc) + timedelta(hours=8)
                    formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

                    print(f"okx : 持仓量(BTC) : {oi_ccy:.2f}  {formatted_time} ")


asyncio.run(subscribe_open_interest())