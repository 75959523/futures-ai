from fastapi import FastAPI
from fastapi.responses import JSONResponse
import services.data_store

app = FastAPI()

@app.get("/data")
async def get_data():
    return JSONResponse(content={
        "okx_open_interest": services.data_store.okx_open_interest_data,
        "okx_mark_price": services.data_store.okx_mark_price_data,
        "okx_funding_rate": services.data_store.okx_funding_rate_data,
        "binance_open_interest": services.data_store.binance_open_interest_data,
        "binance_funding_rate_data": services.data_store.binance_funding_rate_data,
        "binance_mark_price_data": services.data_store.binance_mark_price_data,
        "bybit_funding_rate_data": services.data_store.bybit_funding_rate_data,
        "bybit_mark_price_data":services.data_store.bybit_mark_price_data
    })