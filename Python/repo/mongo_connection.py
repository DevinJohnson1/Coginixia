"""MongoDB connection and configuration"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "coginixia")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]

# Collections
customers_collection = db["customers"]
accounts_collection = db["accounts"]
admins_collection = db["admins"]
users_collection = db["users"]
sessions_collection = db["sessions"]


def clear_all_collections():
    """Clear all collections from the database."""
    customers_collection.delete_many({})
    accounts_collection.delete_many({})
    admins_collection.delete_many({})
    users_collection.delete_many({})
    sessions_collection.delete_many({})


def init_indexes():
    """Create indexes on collections for better query performance."""
    customers_collection.create_index("id", unique=True)
    accounts_collection.create_index("id", unique=True)
    admins_collection.create_index("id", unique=True)
    users_collection.create_index("id", unique=True)
    users_collection.create_index("username", unique=True)
    sessions_collection.create_index("token", unique=True)
    sessions_collection.create_index("user_id")