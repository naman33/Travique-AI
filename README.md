# Travique AI

An AI-powered travel itinerary generator that creates personalised day-by-day 
travel plans based on your destination, budget, interests, and food preferences.

Built with Python, Streamlit, and Google Gemini 2.5 Flash.

**Live app:** https://travique-ai.streamlit.app

---

## What it does

- Generates complete day-by-day itineraries with timings and real place names
- Fetches live weather for your destination and builds weather-aware suggestions
- Adapts to your budget in Indian Rupees (INR)
- Respects food preferences — vegetarian, halal, Jain, street food, and more
- Shows estimated costs per activity in INR
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

## Project structure
Travique-AI/
├── app/
│   ├── main.py              # Streamlit UI and app logic
│   ├── services/
│   │   └── ai_service.py    # Gemini API integration
│   ├── components/          # Reusable UI components (upcoming)
│   ├── pages/               # Multi-page routing (upcoming)
│   └── utils/               # Helper functions (upcoming)
├── data/                    # Datasets and saved itineraries (upcoming)
├── .streamlit/
│   └── config.toml          # Theme and server config
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

**4. Add your API key**

Create a `.env` file in the root folder:
GEMINI_API_KEY=your_gemini_api_key_here

Get a free key at: https://aistudio.google.com

**5. Run the app**
```bash
cd app
streamlit run main.py
```

---

## Deployment

Deployed on Streamlit Community Cloud with secrets managed through 
the Streamlit secrets manager — API keys never touch GitHub.

---

## Roadmap

- [x] AI itinerary generation with Gemini 2.5 Flash
- [x] INR budget system with smart labels
- [x] Live weather integration
- [x] Save and revisit past itineraries
- [ ] Multi-turn travel chatbot for follow-up questions
- [ ] Cloud database (Supabase) for persistent saves on live app
- [ ] Google Maps links for every location
- [ ] PDF export of itineraries

---

## Author

Naman Pal — [github.com/naman33](https://github.com/naman33)
---
*Built with Python, Streamlit, and Google Gemini.