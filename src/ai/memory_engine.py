from src.database.mongodb import db

users = db["user_memory"]

def get_memory(username: str):
    user = users.find_one({"username": username})
    return user.get("memory", []) if user else []

def update_memory(username: str, new_fact: str):
    users.update_one(
        {"username": username},
        {"$push": {"memory": new_fact}},
        upsert=True
    )
