
from db import repository
from cache.redis_client import set_stock


def get_product_stock(product_id: int):
    db_stock = repository.get_stock_from_db(product_id)
    if db_stock is None:
        return None
    set_stock(product_id, db_stock)
    return db_stock


def place_order(customer_id: int, items: list):
    customer = repository.get_customer_by_id(customer_id)
    if not customer:
        raise ValueError("CUSTOMER_NOT_FOUND")

    total_amount = 0
    stock_updates = []

    for item in items:
        product_id = item.product_id
        qty = item.quantity

        product = repository.get_product_by_id(product_id)
        if not product:
            raise ValueError("PRODUCT_NOT_FOUND")

        stock = repository.get_stock_from_db(product_id)
        if stock is None:
            raise ValueError("STOCK_NOT_FOUND")

        if stock < qty:
            raise ValueError("INSUFFICIENT_STOCK")

        new_stock = stock - qty
        stock_updates.append((product_id, new_stock))

        total_amount += product["price"] * qty

    for (product_id, new_stock) in stock_updates:
        repository.update_stock_in_db(product_id, new_stock)
        set_stock(product_id, new_stock)

    order_id = repository.create_order(customer_id, total_amount)

    for item in items:
        repository.add_order_item(order_id, item.product_id, item.quantity)

    return order_id
