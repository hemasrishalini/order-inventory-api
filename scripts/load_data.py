import sqlite3
import random
from config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

cursor.execute("DELETE FROM customers")
cursor.execute("DELETE FROM products")
cursor.execute("DELETE FROM inventory")
cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM order_items")

customers = [
    ("Rahul Sharma", "Mumbai", "rahul@example.com"),
    ("Priya Singh", "Delhi", "priya@example.com"),
    ("Aarav Patel", "Ahmedabad", "aarav@example.com"),
    ("Neha Kulkarni", "Pune", "neha@example.com"),
    ("Rohan Das", "Kolkata", "rohan@example.com"),
]

while len(customers) < 30:
    customers.append((
        f"Customer{len(customers)+1}",
        "CityX",
        f"cust{len(customers)+1}@example.com"
    ))

cursor.executemany(
    "INSERT INTO customers (name, city, email) VALUES (?, ?, ?)",
    customers
)

products = [
    ("Wireless Mouse", "Electronics", 799),
    ("Keyboard", "Electronics", 1199),
    ("USB Cable", "Accessories", 199),
    ("Laptop Stand", "Office", 899),
    ("Water Bottle", "Lifestyle", 399)
]

while len(products) < 20:
    products.append((
        f"Product{len(products)+1}",
        "CategoryX",
        random.randint(100, 2000)
    ))

cursor.executemany(
    "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
    products
)

cursor.execute("SELECT id FROM products")
product_ids = [row[0] for row in cursor.fetchall()]

inventory = []
for pid in product_ids:
    inventory.append((pid, random.randint(20, 200)))

cursor.executemany(
    "INSERT INTO inventory (product_id, stock) VALUES (?, ?)",
    inventory
)

cursor.execute("SELECT id FROM customers")
customer_ids = [row[0] for row in cursor.fetchall()]

order_count = 0

for _ in range(60):
    customer = random.choice(customer_ids)

    total_amount = 0

    cursor.execute(
        "INSERT INTO orders (customer_id, order_date, total_amount) VALUES (?, DATE('now'), 0)",
        (customer,)
    )
    order_id = cursor.lastrowid

    items_for_order = random.randint(1, 5)

    for _ in range(items_for_order):
        product_id = random.choice(product_ids)
        qty = random.randint(1, 3)

        cursor.execute("SELECT price FROM products WHERE id=?", (product_id,))
        price = cursor.fetchone()[0]

        total_amount += price * qty

        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
            (order_id, product_id, qty)
        )

    cursor.execute(
        "UPDATE orders SET total_amount=? WHERE id=?",
        (total_amount, order_id)
    )

conn.commit()
conn.close()
