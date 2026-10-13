
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

print(
    "MONGO_URI configured:",
    bool(os.getenv("MONGO_URI")),
    flush=True
)

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is not configured")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=10000
)

db = client["lost_found_db"]
items_collection = db["items"]

print("MongoDB client initialized!", flush=True)
