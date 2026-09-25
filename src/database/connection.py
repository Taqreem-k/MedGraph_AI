import sqlite3
import json
import os

# Define the database file location at the root of the project
DB_PATH = "medgraph_core.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Table for storing the structured JSON events from the LangGraph output
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timeline_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_date TEXT NOT NULL,
            event_type TEXT NOT NULL,
            description TEXT NOT NULL,
            metrics TEXT, -- We will store the metrics dictionary as a JSON string
            source_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()