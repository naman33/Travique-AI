import sqlite3
import os
from datetime import datetime

# Database file lives in the data/ folder
# Always resolve the database path relative to this file
# Works correctly regardless of where Streamlit runs from
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "travique.db")


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    Creates the database file if it doesn't exist yet.
    
    In SQLite, simply connecting to a file creates it automatically.
    This is very different from PostgreSQL or MySQL where you need
    to manually create the database first.
    """
    conn = sqlite3.connect(DB_PATH)
    # This makes rows behave like dictionaries
    # So you can do row["destination"] instead of row[1]
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Creates the itineraries table if it doesn't exist.
    
    We use CREATE TABLE IF NOT EXISTS — this means we can safely
    call this function every time the app starts without destroying
    existing data. Professional pattern.
    """
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS itineraries (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            destination     TEXT NOT NULL,
            days            INTEGER NOT NULL,
            travelers       INTEGER NOT NULL,
            budget_inr      INTEGER NOT NULL,
            budget_label    TEXT NOT NULL,
            travel_style    TEXT NOT NULL,
            interests       TEXT NOT NULL,
            food_prefs      TEXT NOT NULL,
            itinerary_text  TEXT NOT NULL,
            created_at      TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_itinerary(destination, days, travelers, budget_inr,
                   budget_label, travel_style, interests,
                   food_prefs, itinerary_text):
    """
    Saves one itinerary to the database.
    
    interests and food_prefs are Python lists.
    SQLite can't store lists directly — we join them into
    a comma-separated string. We'll split them back when reading.
    This is called serialization.
    """
    conn = get_connection()

    conn.execute("""
        INSERT INTO itineraries (
            destination, days, travelers, budget_inr,
            budget_label, travel_style, interests,
            food_prefs, itinerary_text, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        destination,
        days,
        travelers,
        budget_inr,
        budget_label,
        travel_style,
        ", ".join(interests) if interests else "General",
        ", ".join(food_prefs) if food_prefs else "No restrictions",
        itinerary_text,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()
    conn.close()


def get_all_itineraries():
    """
    Returns all saved itineraries, newest first.
    
    ORDER BY created_at DESC means most recent at the top.
    We convert each row to a dict so it's easy to work with
    in Streamlit.
    """
    conn = get_connection()

    rows = conn.execute("""
        SELECT * FROM itineraries
        ORDER BY created_at DESC
    """).fetchall()

    conn.close()

    # Convert Row objects to plain dictionaries
    return [dict(row) for row in rows]


def delete_itinerary(itinerary_id):
    """
    Deletes one itinerary by its ID.
    
    The ? placeholder prevents SQL injection — never put
    variables directly into SQL strings. Always use placeholders.
    This is a critical security practice.
    """
    conn = get_connection()

    conn.execute(
        "DELETE FROM itineraries WHERE id = ?",
        (itinerary_id,)
    )

    conn.commit()
    conn.close()


def get_itinerary_count():
    """
    Returns the total number of saved itineraries.
    Useful for showing a count in the UI.
    """
    conn = get_connection()

    count = conn.execute(
        "SELECT COUNT(*) FROM itineraries"
    ).fetchone()[0]

    conn.close()
    return count