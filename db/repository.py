from db.connection import get_connection

#products

def get_all_products(offset: int, limit: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, category, price
        FROM products
        LIMIT ? OFFSET ?
    """, (limit, offset))

    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM products")
    total = cursor.fetchone()[0] #COUNT(*) returns only one value That value is always at index 0

    conn.close()
    return total, rows

def get_product_by_id(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, category, price
        FROM products
        WHERE id = ?
    """, (product_id,))

    row = cursor.fetchone()
    conn.close()
    return row

#customer

def get_customer_by_id(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, city, email
        FROM customers
        WHERE id = ?
    """, (customer_id,))

    row = cursor.fetchone()
    conn.close()
    return row


#orders

def create_order(customer_id: int, total_amount: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO orders (customer_id, order_date, total_amount)
        VALUES (?, DATE('now'), ?)
    """, (customer_id, total_amount))

    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id


def add_order_item(order_id: int, product_id: int, quantity: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO order_items (order_id, product_id, quantity)
        VALUES (?, ?, ?)
    """, (order_id, product_id, quantity))

    conn.commit()
    conn.close()

def get_customer_orders(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, order_date, total_amount
        FROM orders
        WHERE customer_id = ?
        ORDER BY order_date DESC
    """, (customer_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_order_items(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT oi.quantity, p.name as product
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    """, (order_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

#inventory

def get_stock_from_db(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT stock
        FROM inventory
        WHERE product_id = ?
    """, (product_id,))

    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def update_stock_in_db(product_id: int, new_stock: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE inventory
        SET stock = ?
        WHERE product_id = ?
    """, (new_stock, product_id))

    conn.commit()
    conn.close()


#analytics


def get_product_sales():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.name AS product,
               SUM(oi.quantity) AS units_sold,
               SUM(oi.quantity * p.price) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        GROUP BY oi.product_id
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_low_stock(threshold: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.name AS product, i.stock
        FROM inventory i
        JOIN products p ON i.product_id = p.id
        WHERE i.stock < ?
    """, (threshold,))

    rows = cursor.fetchall()
    conn.close()
    return rows