from fastapi import FastAPI
from fastapi.responses import JSONResponse
import services.data_store

app = FastAPI()

@app.get("/data")
async def get_data():
    return JSONResponse(content={
        "okx_open_interest": services.data_store.okx_open_interest,
        "okx_mark_price": services.data_store.okx_mark_price,
        "okx_funding_rate": services.data_store.okx_funding_rate,
        "binance_open_interest": services.data_store.binance_open_interest,
        "binance_funding_rate": services.data_store.binance_funding_rate,
        "binance_mark_price": services.data_store.binance_mark_price,
        "bybit_funding_rate": services.data_store.bybit_funding_rate,
        "bybit_mark_price": services.data_store.bybit_mark_price,
        "bybit_open_interest": services.data_store.bybit_open_interest
    })