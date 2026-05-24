import streamlit as st

# Page configuration — always the first Streamlit command
st.set_page_config(
    page_title="Travique AI",
    page_icon="✈️",
    layout="wide"
)

# Main heading
st.title("✈️ Travique AI")
st.subheader("Your personal AI travel planner")

# A simple divider
st.divider()

# Two columns — left for inputs, right for output
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
            st.info(f"Generating a {days}-day itinerary for {destination}...")
            # AI integration comes in the next step
    else:
        st.markdown(
            "Fill in your trip details on the left and "
            "click **Generate** to create your personalized itinerary."
        )