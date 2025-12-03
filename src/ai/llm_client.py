import requests
from src.config import GROQ_API_KEY

# -------------------------
# CONSTANTS
# -------------------------
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"


# -------------------------
# MAIN FUNCTION
# -------------------------
def groq_generate(prompt: str, temperature: float = 0.7, max_tokens: int = 300) -> str:
    """Generate LLM response using Groq API safely."""
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        res = requests.post(GROQ_URL, json=payload, headers=headers, timeout=15)

        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()

        return f"❌ API Error {res.status_code}: {res.text}"

    except requests.exceptions.Timeout:
        return "⚠️ Timeout: The model took too long to respond."

    except Exception as e:
        return f"❌ Exception: {e}"
