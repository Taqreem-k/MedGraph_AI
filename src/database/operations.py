import json
import sqlite3
from typing import List, Dict, Any
from .connection import get_connection

def save_timeline_events(events: List[Dict[str, Any]], source_file: str, patient_name: str) -> None:
    if not events:
        return

    conn = get_connection()
    cursor = conn.cursor()

    for event in events:
        event_date = event.get("date", "Unknown")
        event_type = event.get("event_type", "Uncategorized")
        description = event.get("description", "")
        
        metrics_dict = event.get("metrics", {})
        metrics_json = json.dumps(metrics_dict) if metrics_dict else None

        cursor.execute('''
            INSERT INTO timeline_events (patient_name, event_date, event_type, description, metrics, source_file)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (patient_name, event_date, event_type, description, metrics_json, source_file))

    conn.commit()
    conn.close()

def get_timeline_events(patient_name: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, event_date, event_type, description, metrics, source_file 
        FROM timeline_events
        WHERE patient_name = ?
        ORDER BY event_date DESC
    ''', (patient_name,))
    
    rows = cursor.fetchall()
    conn.close()

    events = []
    for row in rows:
        event_dict = dict(row)
        if event_dict["metrics"]:
            try:
                event_dict["metrics"] = json.loads(event_dict["metrics"])
            except json.JSONDecodeError:
                event_dict["metrics"] = {}
        else:
            event_dict["metrics"] = {}
        events.append(event_dict)

    return events

def get_all_patients() -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT patient_name FROM timeline_events ORDER BY patient_name ASC')
    rows = cursor.fetchall()
    conn.close()
    
    return [row["patient_name"] for row in rows]