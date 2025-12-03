from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from src.config import MONGO_URI

client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    print("✅ MongoDB connected successfully.")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

db = client["context_retail_ai"]  # database name
