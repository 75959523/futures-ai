from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import data_store

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/data")
async def get_data():
    return data_store.get_market_data()