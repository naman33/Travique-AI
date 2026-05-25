from google import genai
import streamlit as st
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()


def get_api_key():
    """
    Gets the API key from the right place depending on environment.
    
    Local development  → reads from .env file
    Streamlit Cloud    → reads from st.secrets
    
    This is the professional way to handle secrets across environments.
    """
    # Try Streamlit secrets first (production)
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        # Fall back to .env (local development)
        return os.getenv("GEMINI_API_KEY")


def generate_itinerary(destination, days, budget_inr, budget_label,
                       interests, travel_style, food_prefs=None):

    # Get key from the right source
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    interests_str = ", ".join(interests) if interests else "general sightseeing"
    food_str = ", ".join(food_prefs) if food_prefs else "no restrictions"
    total_budget = budget_inr * days

    prompt = f"""
    You are Travique AI, an expert travel planner. Create a detailed, 
    personalised travel itinerary for an Indian traveller.

    TRIP DETAILS:
    - Destination: {destination}
    - Duration: {days} days
    - Daily budget per person: ₹{budget_inr:,} ({budget_label} level)
    - Total trip budget: ₹{total_budget:,}
    - Interests: {interests_str}
    - Travel style: {travel_style}
    - Food preferences: {food_str}

    IMPORTANT: Show all costs in Indian Rupees (₹).
    Convert local currency to INR approximately.
    Respect food preferences strictly.
    If "Desserts & sweets" is in preferences, recommend local desserts each day.

    Use EXACTLY this structure. Always start each day with "DAY" in capitals:

    DAY [number]: [Creative theme for the day]

    Morning (9:00 AM):
    - Activity: [specific real place with 1-line description]
    - Estimated cost: ₹[amount]

    Afternoon (1:00 PM):
    - Activity: [specific real place with 1-line description]
    - Estimated cost: ₹[amount]

    Evening (6:00 PM):
    - Activity: [specific real place]
    - Restaurant: [real restaurant name, cuisine, price per person ₹]

    Daily budget estimate: ₹[min]–₹[max]

    ---

    After all days add:

    TRAVEL TIPS:
    - [3 practical tips specific to this destination]

    BEST TIME TO VISIT:
    - [One sentence with specific months]

    Be specific. Use real place names and real restaurants.
    Friendly, enthusiastic tone like a well-travelled friend.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text