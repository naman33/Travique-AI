import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key():
    """Same pattern as ai_service — works locally and on Streamlit Cloud."""
    try:
        return st.secrets["OPENWEATHER_API_KEY"]
    except Exception:
        return os.getenv("OPENWEATHER_API_KEY")


def get_weather(destination):
    """
    Fetches current weather and 5-day forecast for a destination.
    
    OpenWeather's free tier gives us:
    - Current weather (temperature, condition, humidity, wind)
    - 5-day forecast in 3-hour intervals
    
    We return a clean dictionary that's easy to use in the UI
    and easy to pass to the AI prompt.
    """
    api_key = get_api_key()

    if not api_key:
        return None

    try:
        # ── Current weather ───────────────────────────────────
        current_url = "https://api.openweathermap.org/data/2.5/weather"
        current_response = requests.get(current_url, params={
            "q": destination,
            "appid": api_key,
            "units": "metric"  # Celsius
        })

        if current_response.status_code != 200:
            return None

        current = current_response.json()

        # ── 5-day forecast ────────────────────────────────────
        forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        forecast_response = requests.get(forecast_url, params={
            "q": destination,
            "appid": api_key,
            "units": "metric",
            "cnt": 5  # Next 5 data points (covers ~15 hours)
        })

        forecast_data = []
        if forecast_response.status_code == 200:
            forecast_json = forecast_response.json()
            for item in forecast_json["list"]:
                forecast_data.append({
                    "time": item["dt_txt"],
                    "temp": round(item["main"]["temp"]),
                    "condition": item["weather"][0]["description"].title()
                })

        # ── Build clean weather dict ──────────────────────────
        weather = {
            "city": current["name"],
            "country": current["sys"]["country"],
            "temp": round(current["main"]["temp"]),
            "feels_like": round(current["main"]["feels_like"]),
            "condition": current["weather"][0]["description"].title(),
            "humidity": current["main"]["humidity"],
            "wind_speed": round(current["wind"]["speed"] * 3.6),  # m/s to km/h
            "forecast": forecast_data
        }

        return weather

    except Exception:
        return None


def format_weather_for_prompt(weather):
    """
    Converts weather dict into a string we can inject into the AI prompt.
    
    The AI reads this and uses it to make weather-aware suggestions —
    like recommending indoor activities if it's raining, or suggesting
    early morning hikes if it's going to be hot.
    """
    if not weather:
        return "Weather data unavailable."

    forecast_str = ""
    for f in weather["forecast"]:
        forecast_str += f"\n  - {f['time']}: {f['temp']}°C, {f['condition']}"

    return f"""
Current weather in {weather['city']}, {weather['country']}:
- Temperature: {weather['temp']}°C (feels like {weather['feels_like']}°C)
- Condition: {weather['condition']}
- Humidity: {weather['humidity']}%
- Wind: {weather['wind_speed']} km/h

Upcoming forecast:{forecast_str}
"""