import os
from dotenv import load_dotenv

load_dotenv()

# ---- Environment Variables ----
MONGO_URI = os.getenv("MONGO_URI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not MONGO_URI:
    raise Exception("❌ MONGO_URI not found in environment variables.")

if not GROQ_API_KEY:
    raise Exception("❌ GROQ_API_KEY not found in environment variables.")
