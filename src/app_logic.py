from src.ai.llm_client import groq_generate
from src.ai.memory_engine import get_memory, update_memory
from src.database.mongodb import db
from src.utils.environment import get_ip_location, get_weather, classify_weather
from src.utils.store_locator import get_nearest_store


def get_or_create_customer(username: str):
    """Find customer by name or create new user if not found."""

    collection = db["customers"]
    query = {"name": {"$regex": f"^{username}$", "$options": "i"}}

    customer = collection.find_one(query, {"_id": 0})
    
    if customer:
        return customer, False
    
    # Create new entry if not found
    new_customer = {
        "customer_id": f"U{collection.count_documents({}) + 1:04}",
        "name": username,
        "city": None,
        "favorite_category": None,
        "prefers_hot_drinks": None,
        "loyalty_tier": "Basic"
    }

    collection.insert_one(new_customer)
    return new_customer, True



CITY_MAP = {
    "delhi": "New Delhi",
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "mumbai": "Mumbai",
    "chennai": "Chennai",
    "kolkata": "Kolkata",
    "pune": "Pune,IN",
    "hyderabad": "Hyderabad"
}

def extract_city_from_text(message: str):
    msg = message.lower()
    for key, official in CITY_MAP.items():
        if key in msg:
            return official
    return None




def build_context(username: str, message: str):
    """Build final context including memory, weather, location & store."""
    
    customer, new_user = get_or_create_customer(username)

    true_id = customer["customer_id"]
    memory = get_memory(true_id)

    # Detect city
    ip_info = get_ip_location()
    detected_city = extract_city_from_text(message) or customer.get("city") or (ip_info.get("city") if ip_info else None)

    # Fetch weather
    weather = get_weather(detected_city) if detected_city else None

    # Coordinates for distance lookup
    user_lat = user_lon = None
    if ip_info and "coords" in ip_info:
        user_lat, user_lon = map(float, ip_info["coords"].split(","))

    # Nearest store
    nearest_store = None
    distance = None
    if detected_city and user_lat:
        result = get_nearest_store(detected_city, user_lat, user_lon)
        if result:
            nearest_store, distance = result

    return {
        "resolved_id": true_id,
        "new_user": new_user,
        "customer": customer,
        "memory": memory,
        "city": detected_city,
        "weather": weather,
        "nearest_store": nearest_store,
        "distance": distance
    }



def detect_memory_fact(message: str):
    triggers = ["i like", "i love", "my favorite", "i prefer", "i hate", "i always get"]
    msg = message.lower()
    return message.strip() if any(t in msg for t in triggers) else None



def chat(username: str, message: str):
    """Main conversational response: rule-based + AI fallback."""
    
    context = build_context(username, message)

    true_id = context["resolved_id"]
    customer = context["customer"]
    memory = context["memory"]

    # ---- Weather Logic ----
    weather = context["weather"]

    if weather:
        temp = weather["temperature"]
        condition = weather["condition"]
    else:
        temp = None
        condition = "unknown"


    weather_type = classify_weather(temp)


    # ---- Store logic ----
    nearest = context["nearest_store"]
    distance = context["distance"]

    # ---- Construct Smart Human-like Response ----
    response = ""

    # Greeting
    if context["new_user"]:
        response += f"👋 Welcome {username}! Your profile is set up.\n"
    else:
        response += f"Hey {username}, good to see you again!\n"

    # Weather Statement
    if context["city"]:
        response += f"{context['city']} is currently {temp}°C with {condition}. "
    else:
        response += "Couldn't detect your location yet. "

    # Recommendation based on weather category
    if weather_type == "hot":
        suggestion = "a cold brew or iced latte"
    elif weather_type == "cold":
        suggestion = "a hot chocolate or ginger tea"
    else:
        suggestion = "coffee or juice"

    # Store recommendation
    if nearest:
        response += f"There's a {nearest['name']} about {distance} km away — {suggestion} would be perfect. "
    else:
        response += f"{suggestion} would be great right now. "

    # Loyalty-based personalization
    if customer.get("loyalty_tier") in ["Gold", "Platinum"]:
        response += f"💳 As a {customer['loyalty_tier']} member, you might have perks available!"

    # Store new memory if relevant
    new_fact = detect_memory_fact(message)
    if new_fact:
        update_memory(true_id, new_fact)

    return response.strip()
