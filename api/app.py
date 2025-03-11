from fastapi import FastAPI
from fastapi.responses import JSONResponse
from services import data_store

app = FastAPI()

@app.get("/data")
async def get_data():
    return JSONResponse(content=data_store.get_market_data())