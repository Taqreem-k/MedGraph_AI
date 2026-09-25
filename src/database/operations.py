import json
import sqlite3
from typing import List, Dict, Any
from .connection import get_connection

def save_timeline_events(events: List[Dict[str, Any]], source_file: str) -> None:
    if not events:
        return

    conn = get_connection()
    cursor = conn.cursor()

    for event in events:
        # Safely extract data, providing fallbacks if the LLM missed a key
        event_date = event.get("date", "Unknown")
        event_type = event.get("event_type", "Uncategorized")
        description = event.get("description", "")
        
        # The database expects a string for metrics, but our State holds a dictionary
        metrics_dict = event.get("metrics", {})
        metrics_json = json.dumps(metrics_dict) if metrics_dict else None

        cursor.execute('''
            INSERT INTO timeline_events (event_date, event_type, description, metrics, source_file)
            VALUES (?, ?, ?, ?, ?)
        ''', (event_date, event_type, description, metrics_json, source_file))

    conn.commit()
    conn.close()

def get_all_timeline_events() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()

    # Sort by date descending so the most recent medical events appear first
    cursor.execute('''
        SELECT id, event_date, event_type, description, metrics, source_file 
        FROM timeline_events
        ORDER BY event_date DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()

    events = []
    for row in rows:
        # Convert the sqlite3.Row object back into a standard dictionary
        event_dict = dict(row)
        
        # Parse the JSON string back into a dictionary for Streamlit to render easily
        if event_dict["metrics"]:
            try:
                event_dict["metrics"] = json.loads(event_dict["metrics"])
            except json.JSONDecodeError:
                event_dict["metrics"] = {}
        else:
            event_dict["metrics"] = {}
            
        events.append(event_dict)

    return events