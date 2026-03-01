from fastapi import FastAPI, HTTPException
from models.schemas import (
    ProductListResponse,
    ProductStockResponse,
    OrderCreateRequest,
    OrderCreateResponse,
    AllCustomerOrdersResponse,
    AnalyticsResponse,
    LowStockResponse
)
from db import repository
from services.order_service import get_product_stock, place_order

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "UP", "service": "Order Inventory API"}


@app.get("/products", response_model=ProductListResponse)
def list_products(offset: int = 0, limit: int = 20):
    total, rows = repository.get_all_products(offset, limit)
    products = [dict(row) for row in rows]
    return {"total": total, "products": products}


@app.get("/products/{product_id}/stock", response_model=ProductStockResponse)
def product_stock(product_id: int):
    stock = get_product_stock(product_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="PRODUCT_NOT_FOUND")
    return {"product_id": product_id, "stock": stock, "source": "database"}


@app.get("/customers/{customer_id}/orders", response_model=AllCustomerOrdersResponse)
def customer_orders(customer_id: int):
    customer = repository.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="CUSTOMER_NOT_FOUND")

    orders = repository.get_customer_orders(customer_id)
    formatted_orders = []

    for order in orders:
        items = repository.get_order_items(order["id"])
        formatted_orders.append({
            "order_id": order["id"],
            "date": order["order_date"],
            "total": order["total_amount"],
            "items": [{"product": i["product"], "qty": i["quantity"]} for i in items]
        })

    return {"customer": customer["name"], "orders": formatted_orders}


@app.post("/orders", response_model=OrderCreateResponse)
def create_order(request: OrderCreateRequest):
    try:
        order_id = place_order(request.customer_id, request.items)
        return {"order_id": order_id, "status": "CONFIRMED"}
    except ValueError as e:
        if str(e) == "CUSTOMER_NOT_FOUND":
            raise HTTPException(status_code=404, detail="CUSTOMER_NOT_FOUND")
        if str(e) == "PRODUCT_NOT_FOUND":
            raise HTTPException(status_code=404, detail="PRODUCT_NOT_FOUND")
        if str(e) == "INSUFFICIENT_STOCK":
            raise HTTPException(status_code=400, detail="INSUFFICIENT_STOCK")
        raise HTTPException(status_code=500, detail="SERVER_ERROR")


@app.get("/analytics/products", response_model=AnalyticsResponse)
def analytics_products():
    rows = repository.get_product_sales()
    data = {}
    for row in rows:
        data[row["product"]] = {"units_sold": row["units_sold"], "revenue": row["revenue"]}
    return data


@app.get("/analytics/low-stock", response_model=LowStockResponse)
def low_stock(threshold: int = 10):
    rows = repository.get_low_stock(threshold)
    formatted = [{"product": r["product"], "stock": r["stock"]} for r in rows]
    return {"threshold": threshold, "products": formatted}