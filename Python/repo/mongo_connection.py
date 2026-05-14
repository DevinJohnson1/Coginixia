"""MongoDB connection and configuration"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "coginixia")

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]

# Collections
customers_collection = db["customers"]
accounts_collection = db["accounts"]


def init_indexes():
    """Create indexes on collections for better query performance."""
    customers_collection.create_index("id", unique=True)
    accounts_collection.create_index("id", unique=True)