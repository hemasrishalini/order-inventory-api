import time
from cache.redis_client import redis_client
from db import repository

def sync_stock():
    keys = redis_client.keys("product_stock:*")
    for key in keys:
        product_id = int(key.split(":")[1])
        stock = redis_client.get(key)
        if stock is not None:
            repository.update_stock_in_db(product_id, int(stock))

def run_worker():
    while True:
        sync_stock()
        time.sleep(30)

if __name__ == "__main__":
    run_worker()
