import streamlit as st
from services.ai_service import generate_itinerary

st.set_page_config(
    page_title="Travique AI",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Travique AI")
st.subheader("Your personal AI travel planner")
st.divider()

left, right = st.columns([1, 1])

with left:
    st.markdown("### Plan your trip")

    destination = st.text_input(
        "Where do you want to go?",
        placeholder="e.g. Tokyo, Japan"
    )

    days = st.number_input(
        "How many days?",
        min_value=1,
        max_value=30,
        value=5
    )

    budget = st.selectbox(
        "What is your budget?",
        ["Budget (under $50/day)",
         "Mid-range ($50–150/day)",
         "Luxury ($150+/day)"]
    )

    interests = st.multiselect(
        "What are your interests?",
        ["Culture & History", "Food & Cuisine",
         "Adventure & Sports", "Nature & Wildlife",
         "Shopping", "Art & Museums",
         "Nightlife", "Photography"]
    )

    travel_style = st.radio(
        "Travel style?",
        ["Solo", "Couple", "Family", "Group"]
    )

    generate = st.button("Generate My Itinerary ✨", type="primary")

with right:
    st.markdown("### Your itinerary")

    if generate:
        if not destination:
            st.warning("Please enter a destination first.")
        else:
            # Show a spinner while AI is thinking
            with st.spinner("Travique AI is planning your trip..."):
                try:
                    itinerary = generate_itinerary(
                        destination=destination,
                        days=days,
                        budget=budget,
                        interests=interests,
                        travel_style=travel_style
                    )
                    # Display the result
                    st.success("Your itinerary is ready!")
                    st.markdown(itinerary)

                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
    else:
        st.markdown(
            "Fill in your trip details on the left and "
            "click **Generate** to create your personalized itinerary."
        )