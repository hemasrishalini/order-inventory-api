1.SQLite
	small
	simple
	running locally
	learning project
	inside Docker
	doesn’t need a full database server
	SQLite is the easiest and fastest option.
2.🔵 Earlier Projects → MySQL

Database lived inside MySQL server
You never saw any file.

🟢 This Project → SQLite

Database lives inside a file called orders.db
So you will see the file.

3.🏠 Your project is like a small shop.
Inside your shop, you need a book to write:
how many products you have
how many orders people bought
This book is called:
📘 orders.db
You do NOT create it.
Your Python program will create this notebook when needed.


4.__file__ → this file (config.py)

abspath(__file__) → full path of config.py
Example: /home/shalini/order-inventory-api/config.py

dirname(...) → remove file name → give folder path
/home/shalini/order-inventory-api

5.Your computer has two types of memory:
Slow storage → database (SQLite/MySQL)
Fast memory → Redis
✔ Without Redis
API will read from database every time → SLOW
✔ With Redis
API reads from fast memory → SUPER FAST


5.Redis is a memory box running on your computer.
To talk to that memory box, Python needs a remote control.
redis.StrictRedis is that remote control.
👉 It is the object that lets Python talk to Redis.

Without it:

❌ You cannot set stock
❌ You cannot get stock
❌ You cannot delete stock
❌ Redis cannot be used at all

order service py   
"""
    Returns stock and source: ('cache' or 'database')
    """
"""
    Main order workflow:
    1. Validate customer exists
    2. Validate product + stock
    3. Deduct stock
    4. Create order + items
    5. Update Redis
    """



config.py
connection.py
repository.py
schemas.py
redis_client.py
order_service.py
app.py
load_data.py
stock_worker.py
requirement.txt
dockerfile
docker-compose-yml
readme.md




sudo apt update
sudo apt install sqlite3
sqlite3 --version
nano scripts/create_tables.sql
sqlite3 ../orders.db < create_tables.sql(no output = success)
sqlite3 orders.db ".tables"(shows tables names)
python3 -m scripts.load_data(with no errors, meaning your database has been successfully filled with sample data.)
sqlite3 orders.db "SELECT COUNT(*) FROM customers;"
sqlite3 orders.db "SELECT COUNT(*) FROM products;"
sqlite3 orders.db "SELECT COUNT(*) FROM orders;"
sqlite3 orders.db "SELECT COUNT(*) FROM order_items;"
sqlite3 orders.db "SELECT COUNT(*) FROM inventory;"
🎉 PERFECT! Your database is fully ready.
All counts match exactly what we expected:

✅ 30 customers

✅ 20 products

✅ 60 orders

✅ 171 order_items (correct — more than orders)

✅ 20 inventory rows (equal to products)

how to build docker? install docker engine and docker compose plugin

1.sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg(add docker gpg key)
2.echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null(add docker repo)

3.sudo apt update
4.sudo apt install docker-compose-plugin
5.docker compose version(Docker Compose v5.1.0 is installed and working perfectly.)
6.docker compose build(Docker build completed)
7.docker compose up(start all services like start fastapi, redis...)
8.touch cache/__init__.py
touch db/__init__.py
touch models/__init__.py
touch services/__init__.py
touch workers/__init__.py
touch scripts/__init__.py
9.docker compose build --no-cache
10.docker compose up
11. localhost ---> redis

api tested and working...
1. open postman 
http://localhost:8000/products (get)
http://localhost:8000/products/1/stock (get)
http://localhost:8000/orders (post)---.raw --body---json({
  "customer_id": 1,
  "items": [
    { "product_id": 3, "quantity": 2 },
    { "product_id": 5, "quantity": 1 }
  ]
})
http://localhost:8000/customers/1/orders (get)
http://localhost:8000/products/3/stock (get)
http://localhost:8000/products/5/stock (get)
http://localhost:8000/analytics/products (get)
http://localhost:8000/analytics/low-stock?threshold=10 (get)


how to push to github
1.open github
2.new repository
3.api name
4.create repository

