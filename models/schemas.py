from pydantic import BaseModel, RootModel
from typing import List, Optional

class Product(BaseModel):
    id: int
    name: str
    category: str
    price: int


class ProductListResponse(BaseModel):
    total: int
    products: List[Product]


class ProductStockResponse(BaseModel):
    product_id: int
    stock: int
    source: str #redis cache or sqlite database

class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int


class OrderCreateRequest(BaseModel):
    customer_id: int
    items: List[OrderItemRequest]


class OrderItemResponse(BaseModel):
    product: str
    qty: int


class CustomerOrderResponse(BaseModel):
    order_id: int
    date: str
    total: int
    items: List[OrderItemResponse]


class AllCustomerOrdersResponse(BaseModel):
    customer: str
    orders: List[CustomerOrderResponse]


class OrderCreateResponse(BaseModel):
    order_id: int
    status: str

class ProductAnalytics(BaseModel):
    units_sold: int
    revenue: int


class AnalyticsResponse(RootModel[dict]):
    pass


class LowStockItem(BaseModel):
    product: str
    stock: int


class LowStockResponse(BaseModel):
    threshold: int
    products: List[LowStockItem]