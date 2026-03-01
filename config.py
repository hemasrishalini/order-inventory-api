import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #your project’s folder location

DATABASE_PATH = os.path.join(BASE_DIR, "orders.db")#Put the data (orders.db) inside the project folder.

REDIS_HOST = "redis" # localhost is own computer
REDIS_PORT = 6379 #redis default port
REDIS_DB = 0 #0 determine the firstbox
