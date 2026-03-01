import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True  # return strings instead of bytes
)

def get_stock(product_id: int):
    key = f"product_stock:{product_id}"
    value = redis_client.get(key)
    return value  # returns string or None


def set_stock(product_id: int, stock: int):
    key = f"product_stock:{product_id}"
    redis_client.set(key, stock)


def delete_stock(product_id: int):
    key = f"product_stock:{product_id}"
    redis_client.delete(key)