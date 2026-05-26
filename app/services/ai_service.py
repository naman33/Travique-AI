from google import genai
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY")


def generate_itinerary(destination, days, budget_inr, budget_label,
                       interests, travel_style, food_prefs=None,
                       weather_info=None):

    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    interests_str = ", ".join(interests) if interests else "general sightseeing"
    food_str = ", ".join(food_prefs) if food_prefs else "no restrictions"
    total_budget = budget_inr * days

    weather_section = ""
    if weather_info:
        weather_section = f"""
CURRENT WEATHER DATA:
{weather_info}

Use this weather data to:
- Suggest indoor alternatives if rain is expected
- Recommend early morning activities if afternoon heat is forecast
- Mention what to pack based on conditions
- Adjust the itinerary timing based on weather
"""

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

    {weather_section}

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