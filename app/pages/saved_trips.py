import streamlit as st
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from data.database import get_all_itineraries, delete_itinerary, get_itinerary_count

st.set_page_config(
    page_title="Saved Trips — Travique AI",
    page_icon="✈️",
    layout="wide"
)

st.title("Saved Trips")
st.caption("All your previously generated itineraries")
st.divider()

# Get all saved itineraries
itineraries = get_all_itineraries()
count = get_itinerary_count()

if count == 0:
    st.info("You have no saved itineraries yet. Generate one and click Save.")
else:
    st.markdown(f"**{count} saved trip(s)**")
    st.markdown("<br>", unsafe_allow_html=True)

    for trip in itineraries:
        # Each trip gets a clean expander card
        with st.expander(
            f"📍 {trip['destination']} — "
            f"{trip['days']} days · "
            f"{trip['budget_label']} · "
            f"{trip['created_at']}"
        ):
            # Trip metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Destination**  \n{trip['destination']}")
                st.markdown(f"**Duration**  \n{trip['days']} days")
            with col2:
                st.markdown(f"**Travelers**  \n{trip['travelers']}")
                st.markdown(f"**Budget**  \n₹{trip['budget_inr']:,}/day ({trip['budget_label']})")
            with col3:
                st.markdown(f"**Travel style**  \n{trip['travel_style']}")
                st.markdown(f"**Saved on**  \n{trip['created_at']}")

            st.markdown(f"**Interests:** {trip['interests']}")
            st.markdown(f"**Food preferences:** {trip['food_prefs']}")
            st.divider()

            # Show the full itinerary in tabs
            sections = trip['itinerary_text'].split("DAY ")
            intro = sections[0].strip()
            day_sections = sections[1:]

            if intro:
                st.markdown(intro)

            if day_sections:
                tabs = st.tabs([f"Day {i+1}" for i in range(len(day_sections))])
                for i, tab in enumerate(tabs):
                    with tab:
                        st.markdown(f"**DAY {day_sections[i]}**")
            else:
                st.markdown(trip['itinerary_text'])

            st.divider()

            # Action buttons
            dl_col, del_col = st.columns([3, 1])

            with dl_col:
                st.download_button(
                    label="Download",
                    data=trip['itinerary_text'],
                    file_name=f"Travique_{trip['destination']}_{trip['days']}days.txt",
                    mime="text/plain",
                    key=f"dl_{trip['id']}"
                )

            with del_col:
                if st.button(
                    "Delete",
                    key=f"del_{trip['id']}",
                    type="secondary"
                ):
                    delete_itinerary(trip['id'])
                    st.rerun()