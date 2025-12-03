# 🤖 **ContextRetail AI — The Smart Store Assistant**

> **Tagline:** A context-aware AI shopping assistant that combines user behavior, store data, and real-time environmental signals to deliver highly personalized recommendations, just like a human retail associate, but smarter.
> live --> https://huggingface.co/spaces/Sagar8528/Context_Retail_AI

---

## 1️⃣ The Problem (Real-World Scenario)

Modern brick-and-mortar stores have *zero personalization.*

If a customer walks into Starbucks:

* No one remembers their last order
* No one knows whether they prefer sweet or strong
* No one knows if they’re cold, sick, tired, or just browsing

Meanwhile, online platforms like Amazon use behavioral and contextual signals to boost conversions — *physical stores don’t.*

> **My Solution:** Build an AI retail assistant that behaves like a real store associate, capable of remembering users, understanding their needs, and making *contextually smart product suggestions* in real time.

---

## 2️⃣ Expected User Experience

**For End Customers:**

* No onboarding
* No forms
* No manual input about preferences

Just:

```
User: "I’m freezing today."  
Bot → “There’s a Starbucks 50m away — your favorite caramel latte is in stock, and there’s a 10% discount today. Want it?”
```

**For Store Owners:**

* One-time dataset upload (inventory + offers + metadata)
* System learns customer behavior automatically over time
* No manual re-training or schema work during usage

---

## 3️⃣ Technical Approach

The system combines:

* **Static store knowledge** (menu, pricing, offers, stock)
* **Dynamic customer signals** (preferences, repeated patterns, emotional tone)
* **External context** (location, weather)
* **LLM-based reasoning** for natural conversation

### 🧩 System Intelligence Pipeline

```
🗣 User Message
        ↓
[1] Intent Detection
        ↓
[2] Context Gathering:
      - User memory (dynamic)
      - Store DB (static)
      - Location + Weather APIs (dynamic external)
        ↓
[3] Decision Engine
    (ranking + scoring logic)
        ↓
[4] LLM Response Generation
        ↓
[5] Memory Update (only if new useful info detected)
        ↓
💬 Reply to User
```

---

### How It Works Under the Hood

1. **Intent Engine:**
   Extracts meaning from user messages (e.g., *“cold” → comfort drink intent*).

2. **Context Fusion:**
   Combines:

   * User purchase history
   * Inventory availability
   * Offers
   * Geolocation
   * Weather data

3. **Decision Engine:**
   A scoring system selects the optimal recommendation based on patterns, behavioral signals, and environmental cues.

4. **Generative Layer:**
   The selected reasoning context is passed to **Gemini or Groq**, which generates a natural conversational response — not just a raw database fact dump.

5. **Memory Update:**
   If the user reveals new preference or behavioral insight, it's parsed via an LLM classifier and stored in MongoDB.

---

## 4️⃣ Tech Stack

| Layer                    | Technology                               |
| ------------------------ | ---------------------------------------- |
| Language                 | Python                                   |
| AI Models                | Gemini 2.5 or Groq Llama                 |
| Database                 | MongoDB Atlas                            |
| Vector Search (Optional) | MongoDB Atlas Vector Index               |
| Weather + Geo            | OpenWeather API + Browser Geolocation    |
| Frontend                 | Gradio (demo) / Flutter (mobile version) |

---

## 5️⃣ Challenges & Learnings

🔹 **Challenge: Context Overload**
LLMs hallucinate when given raw database dumps.

**Solution:** Build a structured JSON prompt with relevant items only (top-ranked by scoring engine).

---

🔹 **Challenge: Long-Term Personalization Without Noise**

Blindly storing full chat logs leads to garbage memory.

**Solution:** An extraction pipeline classifies messages into:

```json
{
  "likes": [],
  "dislikes": [],
  "patterns": [],
  "intent": null,
  "contextual_state": null
}
```

Only meaningful signals persist.

---

## 6️⃣ Demo Screenshots (To Be Added)

* 📍 Location-aware recommendations
* 🧠 Memory-based personalized suggestion
* 🎯 Offer-optimized fallback behavior

---
