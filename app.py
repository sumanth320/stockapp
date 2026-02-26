from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import requests
import os

app = FastAPI()

# This route serves your HTML file when you go to http://localhost:8000
@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/api/stock/{symbol}")
def get_stock(symbol: str):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        # Extracting the current price from the Yahoo Finance JSON structure
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        return {"symbol": symbol.upper(), "price": price}
    except Exception as e:
        return {"error": "Invalid ticker or API issue"}