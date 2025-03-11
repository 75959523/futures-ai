import asyncio
import threading
import uvicorn
from services.binance_ws import start_binance_ws
from services.okx_ws import subscribe_open_interest, subscribe_mark_price, subscribe_funding_rate
from services.bybit_ws import subscribe_bybit_funding_rate

from services.binance_api import poll_binance_open_interest
from api.app import app

async def run_tasks():
    await asyncio.gather(
        subscribe_open_interest(),
        subscribe_mark_price(),
        subscribe_funding_rate(),
        subscribe_bybit_funding_rate(),
        asyncio.to_thread(poll_binance_open_interest)
    )

def run_binance_ws():
    binance_thread = threading.Thread(target=start_binance_ws, daemon=True)
    binance_thread.start()

if __name__ == "__main__":
    # 启动 Binance WebSocket(独立线程)
    run_binance_ws()

    # 启动 FastAPI 服务
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)

    # 同时运行 WebSocket 订阅、API 轮询和 FastAPI 服务
    loop = asyncio.get_event_loop()
    loop.create_task(run_tasks())
    loop.run_until_complete(server.serve())