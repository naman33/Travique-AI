# Travique AI

An AI-powered travel itinerary generator that creates personalised day-by-day 
travel plans based on your destination, budget, interests, and food preferences.

Built with Python, Streamlit, and Google Gemini 2.5 Flash.

**Live app:** https://travique-ai.streamlit.app  
**GitHub:** https://github.com/naman33/Travique-AI

---

## Screenshots

### Homepage
![Homepage](docs/screenshots/screenshot-home.png)

### Planning form
![Form](docs/screenshots/screenshot-form.png)

### Generated itinerary
![Itinerary](docs/screenshots/screenshot-itinerary.png)

### AI travel chatbot
![Chatbot](docs/screenshots/screenshot-chat.png)

---

## What it does

- Generates complete day-by-day itineraries with real place names and timings
- Fetches live weather for your destination and builds weather-aware suggestions
- Adapts to your budget in Indian Rupees (INR) with smart budget labels
- Respects food preferences — vegetarian, halal, Jain, street food, and more
- Shows estimated costs per activity in INR
- Multi-turn AI chatbot — modify the itinerary, get packing tips, ask anything
- Save itineraries locally and revisit past trips
- Download any itinerary as a text file for offline use

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend + Backend | Streamlit |
| AI Model | Google Gemini 2.5 Flash |
| Weather Data | OpenWeather API |
| Database | SQLite |
| Language | Python 3.13 |
| Deployment | Streamlit Community Cloud |
| Version Control | Git + GitHub |

---

## Architecture
User Input (Streamlit Sidebar)
↓
Weather Service → OpenWeather API
↓
AI Service → Google Gemini 2.5 Flash
↓
Itinerary Display (Tabbed by Day)
↓
Travel Chatbot (Context-aware follow-ups)
↓
SQLite Database (Save / View / Delete)

---

## Project structure
Travique-AI/
├── app/
│   ├── main.py                  # Streamlit UI and app logic
│   ├── services/
│   │   ├── ai_service.py        # Gemini API integration
│   │   ├── weather_service.py   # OpenWeather API integration
│   │   └── chat_service.py      # Multi-turn chatbot logic
│   └── pages/
│       └── saved_trips.py       # Saved itineraries page
├── data/
│   └── database.py              # SQLite CRUD operations
├── .streamlit/
│   └── config.toml              # Theme and server config
├── requirements.txt
└── README.md

---

## Run locally

**1. Clone the repository**
```bash
git clone https://github.com/naman33/Travique-AI.git
cd Travique-AI
```

**2. Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API keys**

Create a `.env` file in the root folder:
GEMINI_API_KEY=your_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here

Get keys at:
- Gemini: https://aistudio.google.com
- OpenWeather: https://openweathermap.org/api

**5. Run the app**
```bash
cd app
streamlit run main.py
```

---

## Deployment

Deployed on Streamlit Community Cloud with secrets managed through
the Streamlit secrets manager — API keys never touch GitHub.

Auto-deploys on every push to `main`.

---

## Roadmap

- [x] AI itinerary generation with Gemini 2.5 Flash
- [x] INR budget system with smart labels
- [x] Live weather integration
- [x] Save and revisit past itineraries
- [x] Multi-turn travel chatbot
- [ ] Cloud database (Supabase) for persistent saves on live app
- [ ] Google Maps links for every location
- [ ] PDF export of itineraries

---

## Author

Naman Pal — [github.com/naman33](https://github.com/naman33)