import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from services.ai_service import generate_itinerary

st.set_page_config(
    page_title="Travique AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }
    [data-testid="stSidebar"] label {
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #888;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .summary-card {
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border: 1px solid #667eea44;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .budget-tag {
        display: inline-block;
        background: #667eea33;
        border: 1px solid #667eea66;
        border-radius: 6px;
        padding: 2px 10px;
        font-size: 0.78rem;
        color: #a89ef5;
        margin-top: 4px;
    }
    div[data-testid="stNumberInput"] input {
        font-size: 0.95rem;
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
        min_value=500,
        max_value=500000,
        value=5000,
        step=500
    )

    level = budget_label(budget_inr)
    total = budget_inr * int(days) * int(travelers)
    st.markdown(
        f'<span class="budget-tag">'
        f'{level} · {format_inr(budget_inr)}/day · '
        f'Total {format_inr(total)}'
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
        ["Culture & History", "Food & Cuisine",
         "Adventure & Sports", "Nature & Wildlife",
         "Shopping", "Art & Museums", "Nightlife",
         "Photography", "Architecture", "Spiritual & Temples",
         "Local Experiences", "Beaches", "Trekking & Hiking"],
        default=["Culture & History", "Food & Cuisine"]
    )

    food_prefs = st.multiselect(
        "Food preferences",
        ["No restrictions", "Vegetarian", "Vegan",
         "Non-vegetarian", "Eggetarian", "Halal",
         "Jain food", "Gluten-free", "Street food",
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

if generate:
    if not destination:
        st.warning("Please enter a destination in the sidebar.")
    else:
        status = st.empty()
        progress = st.progress(0)

        status.info("Researching your destination...")
        progress.progress(25)

        status.info("Planning your day-by-day route...")
        progress.progress(55)

        try:
            itinerary_text = generate_itinerary(
                destination=destination,
                days=int(days),
                budget_inr=budget_inr,
                budget_label=level,
                interests=interests,
                travel_style=travel_style,
                food_prefs=food_prefs
            )

            progress.progress(90)
            status.info("Finalising your itinerary...")
            progress.progress(100)
            status.empty()
            progress.empty()

            # ── Summary card ──────────────────────────────────
            st.markdown(f"""
            <div class="summary-card">
                <h2 style="margin:0 0 0.4rem 0">📍 {destination}</h2>
                <p style="margin:0; color:#aaa; font-size:0.9rem">
                    {int(days)} days &nbsp;·&nbsp;
                    {int(travelers)} traveller(s) &nbsp;·&nbsp;
                    {level} &nbsp;·&nbsp;
                    {travel_style}
                </p>
                <p style="margin:0.3rem 0 0 0; color:#aaa; font-size:0.9rem">
                    {format_inr(budget_inr)}/day per person
                    &nbsp;·&nbsp;
                    Total estimate ₹{total:,}
                </p>
            </div>
            """, unsafe_allow_html=True)

            # ── Day tabs ──────────────────────────────────────
            sections = itinerary_text.split("DAY ")
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
                st.markdown(itinerary_text)

            st.divider()
            st.download_button(
                label="Download Itinerary",
                data=itinerary_text,
                file_name=f"Travique_{destination}_{days}days.txt",
                mime="text/plain"
            )

        except Exception as e:
            status.empty()
            progress.empty()
            st.error(f"Something went wrong: {str(e)}")

else:
    # ── Empty state ───────────────────────────────────────────
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