import time
import redis
import requests
import json

redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# Get a free key at: https://www.alphavantage.co/support/#api-key
API_KEY = "xx" #add your personal api key here

def fetch_price(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    try:
        r = requests.get(url)
        data = r.json()
        # Alpha Vantage returns data inside "Global Quote"
        price = data["Global Quote"]["05. price"]
        return {"symbol": symbol, "price": price, "status": "success"}
    except Exception as e:
        return {"symbol": symbol, "price": "N/A", "error": str(e)}

if __name__ == "__main__":
    print("Worker is polling for tasks...")
    while True:
        symbol = redis_client.spop("tracked_tickers")
        if symbol:
            print(f"Processing {symbol}...")
            result = fetch_price(symbol)
            redis_client.setex(symbol, 300, json.dumps(result)) # Cache for 5 mins
            time.sleep(20)
        else:
            time.sleep(3)