import csv
from src.database.mongodb import db

def load_customers(csv_path="data/customers.csv"):
    collection = db["customers"]

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        docs = list(reader)

    if docs:
        collection.delete_many({})  # reset for prototype
        collection.insert_many(docs)
        print(f"✅ Loaded {len(docs)} customer records into MongoDB.")

if __name__ == "__main__":
    load_customers()
