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


def chat_with_travique(
    user_message,
    itinerary_text,
    destination,
    days,
    budget_inr,
    budget_label,
    travel_style,
    chat_history
):
    """
    Multi-turn travel chatbot.
    
    Takes the full itinerary as context so every answer
    is specific to the user's actual trip — not generic advice.
    
    chat_history is a list of dicts:
    [
        {"role": "user", "content": "make day 2 cheaper"},
        {"role": "assistant", "content": "Sure! Here's a budget version..."},
        ...
    ]
    """
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    # Build conversation history as a single string
    history_str = ""
    for msg in chat_history[-6:]:  # Last 6 messages for context
        role = "Traveller" if msg["role"] == "user" else "Travique AI"
        history_str += f"{role}: {msg['content']}\n\n"

    prompt = f"""
You are Travique AI, a friendly and expert travel assistant.
You have already generated a travel itinerary for this traveller.
Your job is to answer their follow-up questions helpfully and specifically.

THEIR TRIP:
- Destination: {destination}
- Duration: {days} days
- Daily budget: ₹{budget_inr:,} ({budget_label})
- Travel style: {travel_style}

THEIR ITINERARY:
{itinerary_text}

CONVERSATION SO FAR:
{history_str}

TRAVELLER'S NEW MESSAGE:
{user_message}

INSTRUCTIONS:
- Answer specifically based on their itinerary above
- If they ask to modify something, give the modified version clearly
- If they ask about costs, always use Indian Rupees (₹)
- If they ask about packing, be specific to the destination and season
- Keep answers concise but helpful
- Be friendly and conversational
- Never make up information — if unsure, say so
- If they ask something unrelated to travel, politely redirect
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text