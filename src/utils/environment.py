import requests

IP_API = "https://ipinfo.io/json"
WEATHER_API_KEY = "0eae6d47815a692e0e5e24dbc7f41ddc"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"


def get_ip_location():
    try:
        res = requests.get(IP_API, timeout=5).json()
        return {
            "city": res.get("city"),
            "coords": res.get("loc")  # "lat,lon"
        }
    except:
        return None


def get_weather(city):
    if not city:
        return None
    
    try:
        url = WEATHER_URL.format(city=city, key=WEATHER_API_KEY)
        res = requests.get(url, timeout=6).json()

        # API success
        if "main" in res:
            return {
                "temperature": round(res["main"]["temp"]),
                "condition": res["weather"][0]["description"]
            }

        # Failed (city not found or quota)
        return None

    except Exception:
        return None



def classify_weather(temp):
    """
    Categorize weather into hot/cold/mild.
    Handles cases where temp may be missing or string.
    """

    try:
        temp = float(temp)
    except:
        return "unknown"

    if temp < 18:
        return "cold"
    elif 18 <= temp <= 28:
        return "mild"
    else:
        return "hot"
