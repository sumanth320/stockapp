import psycopg2
from functools import wraps

def clean_ticker(func):
    @wraps(func)
    def wrapper(symbol, *args, **kwargs):
        return func(symbol.strip().upper(), *args, **kwargs)
    return wrapper

def db_logger(func):
    @wraps(func)
    def wrapper(symbol, *args, **kwargs):
        try:
            conn = psycopg2.connect(host="db", database="stock_db", user="user", password="password")
            cur = conn.cursor()
            cur.execute("INSERT INTO search_history (ticker) VALUES (%s)", (symbol,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"DB Log Error: {e}")
        return func(symbol, *args, **kwargs)
    return wrapper