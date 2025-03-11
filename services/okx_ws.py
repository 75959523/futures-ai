import websockets
import json
from datetime import datetime, timezone, timedelta
from config import OKX_WS_URL
import services.data_store

async def subscribe_open_interest():
    try:
        async with websockets.connect(OKX_WS_URL) as ws:
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
            # print("已发送订阅请求:", json.dumps(subscribe_message, indent=4))

            while True:
                response = await ws.recv()
                data = json.loads(response)
                # print("收到数据:", data)

                if "data" in data:
                    for entry in data["data"]:
                        oi_ccy = float(entry["oiCcy"])
                        ts = int(entry["ts"])

                        dt_object = datetime.fromtimestamp(ts / 1000, tz=timezone.utc) + timedelta(hours=8)
                        formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

                        services.data_store.okx_open_interest_data = {
                            "open_interest": round(oi_ccy, 2),
                            "timestamp": formatted_time
                        }
                        # print("更新 open_interest_data:", services.data_store.open_interest_data)  # 打印更新后的数据
    except Exception as e:
        print(f"OKX WebSocket 连接或订阅失败: {e}")

async def subscribe_mark_price():
    try:
        async with websockets.connect(OKX_WS_URL) as ws:
            subscribe_message = {
                "op": "subscribe",
                "args": [
                    {
                        "channel": "mark-price",
                        "instId": "BTC-USDT-SWAP"
                    }
                ]
            }
            await ws.send(json.dumps(subscribe_message))
            # print("已发送订阅请求:", json.dumps(subscribe_message, indent=4))

            while True:
                response = await ws.recv()
                data = json.loads(response)
                # print("收到数据:", data)

                if "data" in data:
                    for entry in data["data"]:
                        try:
                            mark_price = float(entry["markPx"])
                            ts = int(entry["ts"])

                            dt_object = datetime.fromtimestamp(ts / 1000, tz=timezone.utc) + timedelta(hours=8)
                            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

                            # 更新全局变量
                            services.data_store.okx_mark_price_data = {
                                "mark_price": round(mark_price, 2),
                                "timestamp": formatted_time
                            }
                            # print("更新 mark_price_data:", services.data_store.mark_price_data)
                        except KeyError as e:
                            print(f"数据解析错误，缺少字段: {e}")
                        except ValueError as e:
                            print(f"数据格式错误: {e}")
    except Exception as e:
        print(f"OKX WebSocket 连接或订阅失败: {e}")

async def subscribe_funding_rate():
    try:
        async with websockets.connect(OKX_WS_URL) as ws:
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
            # print("已发送订阅请求:", json.dumps(subscribe_message, indent=4))

            while True:
                response = await ws.recv()
                data = json.loads(response)
                # print("收到数据:", data)

                if "data" in data:
                    for entry in data["data"]:
                        funding_rate = float(entry["fundingRate"]) * 100
                        ts = int(entry["ts"])

                        dt_object = datetime.fromtimestamp(ts / 1000, tz=timezone.utc) + timedelta(hours=8)
                        formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

                        # 更新全局变量
                        services.data_store.okx_funding_rate_data = {
                            "funding_rate": f"{funding_rate:.6f}%",
                            "timestamp": formatted_time
                        }
                        # print("更新 funding_rate_data:", services.data_store.okx_funding_rate_data)
    except Exception as e:
        print(f"OKX WebSocket 连接或订阅失败: {e}")