import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import generate_itinerary
from data.database import init_db, save_itinerary
from services.weather_service import get_weather, format_weather_for_prompt
from services.chat_service import chat_with_travique

init_db()

st.set_page_config(
    page_title="Travique AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #1a1a2e; }
    [data-testid="stSidebar"] label {
        font-size: 0.8rem; font-weight: 600;
        letter-spacing: 0.05em; text-transform: uppercase; color: #888;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; border: none; padding: 0.75rem;
        border-radius: 10px; font-size: 0.95rem;
        font-weight: 600; letter-spacing: 0.02em;
    }
    .summary-card {
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border: 1px solid #667eea44; border-radius: 12px;
        padding: 1.5rem; margin-bottom: 1.5rem;
    }
    .budget-tag {
        display: inline-block; background: #667eea33;
        border: 1px solid #667eea66; border-radius: 6px;
        padding: 2px 10px; font-size: 0.78rem;
        color: #a89ef5; margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)


def format_inr(amount):
    if amount >= 100000:
        return f"₹{amount/100000:.1f}L"
    elif amount >= 1000:
        return f"₹{amount/1000:.0f}K"
    return f"₹{amount}"


def budget_label(amount):
    if amount < 1500:
        return "Backpacker"
    elif amount < 4000:
        return "Budget"
    elif amount < 10000:
        return "Mid-range"
    elif amount < 25000:
        return "Comfort"
    else:
        return "Luxury"


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Travique AI")
    st.caption("Personal AI travel planner")
    st.divider()

    destination = st.text_input(
        "Destination",
        placeholder="e.g. Tokyo, Bali, Paris"
    )

    col1, col2 = st.columns(2)
    with col1:
        days = st.number_input("Duration (days)", min_value=1, max_value=30, value=5)
    with col2:
        travelers = st.number_input("Travelers", min_value=1, max_value=20, value=1)

    budget_inr = st.number_input(
        "Daily budget per person (₹)",
        min_value=500, max_value=500000, value=5000, step=500
    )

    level = budget_label(budget_inr)
    total = budget_inr * int(days) * int(travelers)
    st.markdown(
        f'<span class="budget-tag">'
        f'{level} · {format_inr(budget_inr)}/day · Total {format_inr(total)}'
        f'</span>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    travel_style = st.selectbox(
        "Travel style",
        ["Solo adventurer", "Couple", "Family with kids",
         "Group of friends", "Business", "Backpacker"]
    )

    interests = st.multiselect(
        "Interests",
        ["Culture & History", "Food & Cuisine", "Adventure & Sports",
         "Nature & Wildlife", "Shopping", "Art & Museums", "Nightlife",
         "Photography", "Architecture", "Spiritual & Temples",
         "Local Experiences", "Beaches", "Trekking & Hiking"],
        default=["Culture & History", "Food & Cuisine"]
    )

    food_prefs = st.multiselect(
        "Food preferences",
        ["No restrictions", "Vegetarian", "Vegan", "Non-vegetarian",
         "Eggetarian", "Halal", "Jain food", "Gluten-free", "Street food",
         "Fine dining", "Seafood", "Desserts & sweets",
         "Local cuisine only", "No spicy food"],
        default=["No restrictions"]
    )

    st.divider()
    generate = st.button("Generate Itinerary", type="primary")


# ── Main area ─────────────────────────────────────────────────
st.title("Travique AI")
st.caption("Personalised day-by-day travel plans powered by Gemini AI")
st.divider()

# ── Generate ──────────────────────────────────────────────────
if generate:
    if not destination:
        st.warning("Please enter a destination in the sidebar.")
    else:
        status = st.empty()
        progress = st.progress(0)

        try:
            status.info("Fetching live weather data...")
            progress.progress(20)
            weather = get_weather(destination)
            weather_info = format_weather_for_prompt(weather) if weather else None

            status.info("Planning your day-by-day route...")
            progress.progress(50)

            itinerary_text = generate_itinerary(
                destination=destination,
                days=int(days),
                budget_inr=budget_inr,
                budget_label=level,
                interests=interests,
                travel_style=travel_style,
                food_prefs=food_prefs,
                weather_info=weather_info
            )

            progress.progress(90)
            status.info("Finalising your itinerary...")
            progress.progress(100)
            status.empty()
            progress.empty()

            if not itinerary_text:
                st.error("AI returned empty response. Please try again.")
            else:
                st.session_state["itinerary_text"] = itinerary_text
                st.session_state["last_destination"] = destination
                st.session_state["last_days"] = int(days)
                st.session_state["last_travelers"] = int(travelers)
                st.session_state["last_budget_inr"] = budget_inr
                st.session_state["last_level"] = level
                st.session_state["last_travel_style"] = travel_style
                st.session_state["last_interests"] = interests
                st.session_state["last_food_prefs"] = food_prefs
                st.session_state["already_saved"] = False
                st.session_state["weather"] = weather

        except Exception as e:
            status.empty()
            progress.empty()
            st.error(f"Something went wrong: {str(e)}")


# ── Display itinerary ─────────────────────────────────────────
if "itinerary_text" in st.session_state and st.session_state["itinerary_text"]:

    itin = st.session_state["itinerary_text"]
    dest = st.session_state["last_destination"]
    d = st.session_state["last_days"]
    t = st.session_state["last_travelers"]
    b = st.session_state["last_budget_inr"]
    lv = st.session_state["last_level"]
    ts = st.session_state["last_travel_style"]
    total_est = b * d * t
    weather = st.session_state.get("weather")

    # Weather string for summary card
    weather_str = ""
    if weather:
        weather_str = (
            f'<p style="margin:0.5rem 0 0 0; color:#aaa; font-size:0.9rem">'
            f'{weather["city"]} · {weather["temp"]}°C · '
            f'{weather["condition"]} · '
            f'{weather["humidity"]}% humidity · '
            f'{weather["wind_speed"]} km/h wind'
            f'</p>'
        )

    # Summary card
    st.markdown(f"""
    <div class="summary-card">
        <h2 style="margin:0 0 0.4rem 0">📍 {dest}</h2>
        <p style="margin:0; color:#aaa; font-size:0.9rem">
            {d} days &nbsp;·&nbsp; {t} traveller(s) &nbsp;·&nbsp;
            {lv} &nbsp;·&nbsp; {ts}
        </p>
        <p style="margin:0.3rem 0 0 0; color:#aaa; font-size:0.9rem">
            {format_inr(b)}/day per person &nbsp;·&nbsp;
            Total estimate ₹{total_est:,}
        </p>
        {weather_str}
    </div>
    """, unsafe_allow_html=True)

    # Day tabs
    sections = itin.split("DAY ")
    intro = sections[0].strip()
    day_sections = sections[1:]

    if intro:
        st.markdown(intro)
        st.divider()

    if day_sections:
        tabs = st.tabs([f"Day {i+1}" for i in range(len(day_sections))])
        for i, tab in enumerate(tabs):
            with tab:
                st.markdown(f"**DAY {day_sections[i]}**")
    else:
        st.markdown(itin)

    st.divider()

    # Action buttons
    col_save, col_download = st.columns(2)

    with col_save:
        if st.session_state.get("already_saved"):
            st.success("Itinerary already saved.")
        else:
            if st.button("Save Itinerary", type="primary"):
                try:
                    save_itinerary(
                        destination=st.session_state["last_destination"],
                        days=st.session_state["last_days"],
                        travelers=st.session_state["last_travelers"],
                        budget_inr=st.session_state["last_budget_inr"],
                        budget_label=st.session_state["last_level"],
                        travel_style=st.session_state["last_travel_style"],
                        interests=st.session_state["last_interests"],
                        food_prefs=st.session_state["last_food_prefs"],
                        itinerary_text=st.session_state["itinerary_text"]
                    )
                    st.session_state["already_saved"] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not save: {str(e)}")

    with col_download:
        st.download_button(
            label="Download Itinerary",
            data=itin,
            file_name=f"Travique_{dest}_{d}days.txt",
            mime="text/plain"
        )
    # ── Travel Chatbot ────────────────────────────────────────
    st.divider()
    st.markdown("### Ask Travique AI")
    st.caption(
        "Ask anything about your trip — modify the itinerary, "
        "get packing tips, find alternatives, check costs."
    )

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Show suggestion chips for first-time users
    if len(st.session_state["chat_history"]) == 0:
        st.markdown("**Try asking:**")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            if st.button("What should I pack?", key="sugg1"):
                st.session_state["pending_message"] = "What should I pack for this trip?"
        with col_s2:
            if st.button("Make day 1 cheaper", key="sugg2"):
                st.session_state["pending_message"] = "Can you make day 1 more budget friendly?"
        with col_s3:
            if st.button("Best local food?", key="sugg3"):
                st.session_state["pending_message"] = "What are the best local foods I must try?"

    # Display existing chat messages
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle suggestion button clicks
    if "pending_message" in st.session_state:
        pending = st.session_state.pop("pending_message")
        with st.chat_message("user"):
            st.markdown(pending)
        st.session_state["chat_history"].append({
            "role": "user",
            "content": pending
        })
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chat_with_travique(
                    user_message=pending,
                    itinerary_text=st.session_state["itinerary_text"],
                    destination=st.session_state["last_destination"],
                    days=st.session_state["last_days"],
                    budget_inr=st.session_state["last_budget_inr"],
                    budget_label=st.session_state["last_level"],
                    travel_style=st.session_state["last_travel_style"],
                    chat_history=st.session_state["chat_history"]
                )
            st.markdown(reply)
        st.session_state["chat_history"].append({
            "role": "assistant",
            "content": reply
        })
        st.rerun()

    # Chat input box
    user_input = st.chat_input("Ask anything about your trip...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state["chat_history"].append({
            "role": "user",
            "content": user_input
        })
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chat_with_travique(
                    user_message=user_input,
                    itinerary_text=st.session_state["itinerary_text"],
                    destination=st.session_state["last_destination"],
                    days=st.session_state["last_days"],
                    budget_inr=st.session_state["last_budget_inr"],
                    budget_label=st.session_state["last_level"],
                    travel_style=st.session_state["last_travel_style"],
                    chat_history=st.session_state["chat_history"]
                )
            st.markdown(reply)
        st.session_state["chat_history"].append({
            "role": "assistant",
            "content": reply
        })

    # Clear chat button
    if len(st.session_state["chat_history"]) > 0:
        if st.button("Clear chat", key="clear_chat"):
            st.session_state["chat_history"] = []
            st.rerun()

else:
    # Empty state
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **🗺️ Smart planning**

        Builds a complete day-by-day schedule
        with real places, timings, and costs
        in Indian Rupees.
        """)
    with col2:
        st.markdown("""
        **🎯 Personalised**

        Every plan adapts to your budget,
        interests, travel style, and food
        preferences.
        """)
    with col3:
        st.markdown("""
        **📥 Downloadable**

        Save your itinerary as a text file
        and access it offline during
        your trip.
        """)

    st.info("Fill in your trip details in the sidebar and click **Generate Itinerary**")