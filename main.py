import asyncio
import threading
import uvicorn


from services import okx_ws_u, okx_ws_coin, okx_ws_usdc
from services import binance_ws_u, binance_ws_coin, binance_ws_usdc

from services import binance_api_u, binance_api_coin, binance_api_usdc
from services.bybit_ws import subscribe_bybit_funding_rate
from services.bybit_api import poll_bybit_open_interest

from api.app import app

async def run_tasks():
    await asyncio.gather(
        okx_ws_u.subscribe_open_interest(),
        okx_ws_u.subscribe_mark_price(),
        okx_ws_u.subscribe_funding_rate(),
        okx_ws_coin.subscribe_open_interest(),
        okx_ws_coin.subscribe_mark_price(),
        okx_ws_coin.subscribe_funding_rate(),
        okx_ws_usdc.subscribe_open_interest(),
        okx_ws_usdc.subscribe_mark_price(),
        okx_ws_usdc.subscribe_funding_rate(),
        asyncio.to_thread(binance_api_u.poll_binance_open_interest),
        asyncio.to_thread(binance_api_coin.poll_binance_open_interest),
        asyncio.to_thread(binance_api_usdc.poll_binance_open_interest),
        subscribe_bybit_funding_rate(),
        asyncio.to_thread(poll_bybit_open_interest)
    )

def run_binance_ws():
    binance_thread = threading.Thread(target=binance_ws_u.start_binance_ws, daemon=True)
    binance_thread.start()
    binance_thread = threading.Thread(target=binance_ws_coin.start_binance_ws, daemon=True)
    binance_thread.start()
    binance_thread = threading.Thread(target=binance_ws_usdc.start_binance_ws, daemon=True)
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