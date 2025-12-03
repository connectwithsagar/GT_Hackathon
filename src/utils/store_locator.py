import math

# Temporary static store list (replace with real API later)
STORES = [
    {"name": "Starbucks", "city": "Delhi", "lat": 28.6139, "lon": 77.2090},
    {"name": "CCD", "city": "Delhi", "lat": 28.6215, "lon": 77.2150},
    {"name": "Cafe Rio", "city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
]

def _distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    return 2 * R * math.asin(math.sqrt(a))


def get_nearest_store(city, user_lat, user_lon):
    city_stores = [s for s in STORES if s["city"].lower() == city.lower()]
    
    if not city_stores:
        return None
    
    nearest = min(city_stores, key=lambda s: _distance(user_lat, user_lon, s["lat"], s["lon"]))
    dist = round(_distance(user_lat, user_lon, nearest["lat"], nearest["lon"]), 1)
    
    return nearest, dist
