from fastapi import FastAPI
from fastapi.responses import FileResponse
from redis import Redis
import json

app = FastAPI()

# decode_responses=True makes Redis return strings instead of bytes
redis_client = Redis(host='redis', port=6379, db=0, decode_responses=True)

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/api/stock/{symbol}")
def get_stock(symbol: str):
    symbol = symbol.upper()
    
    # 1. Check if we already have the price
    data = redis_client.get(symbol)
    
    if data:
        return json.loads(data)
    
    # 2. If not, add it to the "To-Do List" Set in Redis
    redis_client.sadd("tracked_tickers", symbol)
    
    return {
        "symbol": symbol, 
        "price": "Loading...", 
        "message": "Ticker added to pipeline. Refresh in 10 seconds."
    }