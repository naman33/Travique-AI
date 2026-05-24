from google import genai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()

# Initialize the new client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_itinerary(destination, days, budget, interests, travel_style):
    """
    Takes trip details and returns a complete AI-generated itinerary.
    This is the core function of Travique AI.
    """

    interests_str = ", ".join(interests) if interests else "general sightseeing"

    prompt = f"""
    You are Travique AI, an expert travel planner with deep knowledge of 
    destinations worldwide. Create a detailed, personalized travel itinerary.

    TRIP DETAILS:
    - Destination: {destination}
    - Duration: {days} days
    - Budget: {budget}
    - Interests: {interests_str}
    - Travel Style: {travel_style}

    Create a day-by-day itinerary with this exact structure for each day:

    DAY [number]: [Theme for the day]

    Morning (9:00 AM):
    - Activity with brief description
    - Estimated cost

    Afternoon (1:00 PM):
    - Activity with brief description
    - Estimated cost

    Evening (6:00 PM):
    - Activity with brief description
    - Recommended restaurant with cuisine type

    DAILY BUDGET ESTIMATE: $XX - $XX

    After all days, add:

    TRAVEL TIPS:
    - 3 specific tips for this destination

    BEST TIME TO VISIT: One sentence

    Keep the tone friendly and enthusiastic. Be specific with real place names,
    real restaurants, real attractions. Make it feel like advice from a local friend.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text