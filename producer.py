import time
import requests
import json
from redis import Redis

redis_client = Redis(host='redis', port=6379, db=0, decode_responses=True)

def fetch_and_publish():
    # 1. Pull the latest list of tickers from the Redis Set
    tickers = redis_client.smembers("tracked_tickers")
    
    # If the set is empty, let's track a default so the logs aren't empty
    if not tickers:
        tickers = ["BTC-USD"]
    
    for symbol in tickers:
        print(f"Ingesting: {symbol}")
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            meta = data['chart']['result'][0]['meta']
            payload = {
                "symbol": symbol,
                "price": meta['regularMarketPrice'],
                "timestamp": meta['regularMarketTime']
            }
            
            # Save the specific price data
            redis_client.set(symbol, json.dumps(payload))
            
        except Exception as e:
            print(f"Failed to fetch {symbol}: {e}")

if __name__ == "__main__":
    while True:
        fetch_and_publish()
        print("Cycle complete. Waiting 60 seconds...")
        time.sleep(60)