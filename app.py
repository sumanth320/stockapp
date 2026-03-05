from fastapi import FastAPI
from fastapi.responses import FileResponse
from redis import Redis
import json
from decorators import clean_ticker, db_logger

app = FastAPI()
redis_client = Redis(host='redis', port=6379, db=0, decode_responses=True)

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/api/stock/{symbol}")
@clean_ticker
@db_logger
def get_stock(symbol: str):
    # 1. Check if we have it in Redis
    data = redis_client.get(symbol)
    
    if data:
        return json.loads(data)
    
    # 2. If not, add to the "To-Do List" Set
    redis_client.sadd("tracked_tickers", symbol)
    
    return {
        "symbol": symbol, 
        "price": "Loading...", 
        "message": "Task sent to background worker. Please refresh in a moment."
    }