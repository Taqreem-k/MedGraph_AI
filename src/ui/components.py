import json
import ast
import streamlit as st
from typing import List, Dict, Any

def render_file_uploader():
    st.subheader("📄 Upload Medical Record")
    st.markdown("Upload a PDF, JPG, or PNG to extract structured health data.")
    uploaded_file = st.file_uploader("Select a medical document", type=["pdf", "jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' loaded successfully.")
    return uploaded_file

def render_review_ui(events: List[Dict[str, Any]]) -> tuple[bool, List[Dict[str, Any]]]:
    st.warning("⚠️ **Review Required:** Please verify the AI-extracted data below. Edit any incorrect medication names or vitals before saving.")
    
    edited_events = []
    
    with st.form("clinical_review_form"):
        for i, event in enumerate(events):
            st.markdown(f"### Event {i+1}")
            
            # Formatted text inputs instead of a raw grid
            col1, col2 = st.columns(2)
            with col1:
                new_date = st.text_input("Date", value=event.get("date", ""), key=f"date_{i}")
            with col2:
                new_type = st.text_input("Event Type", value=event.get("event_type", ""), key=f"type_{i}")
                
            new_desc = st.text_area("Clinical Notes & Prescriptions", value=event.get("description", ""), key=f"desc_{i}")
            
            new_metrics = {}
            metrics = event.get("metrics", {})
            
            if metrics:
                st.markdown("**Vitals & Metrics**")
                metric_cols = st.columns(3)
                m_idx = 0
                for k, v in metrics.items():
                    with metric_cols[m_idx % 3]:
                        clean_key = k.replace("_", " ").title()
                        val_str = ", ".join(v) if isinstance(v, list) else str(v)
                        # Render individual input boxes for each metric (e.g., Blood Pressure)
                        new_val = st.text_input(clean_key, value=val_str, key=f"metric_{i}_{k}")
                        new_metrics[k] = new_val
                    m_idx += 1
            else:
                st.caption("No metrics extracted for this event.")
                
            st.divider()
            
            edited_events.append({
                "date": new_date,
                "event_type": new_type,
                "description": new_desc,
                "metrics": new_metrics
            })
            
        submitted = st.form_submit_button("✅ Confirm & Save to Patient Record", type="primary")
        return submitted, edited_events

def render_timeline(events: List[Dict[str, Any]]):
    st.subheader("📅 Patient Health Timeline")
    
    if not events:
        st.info("No timeline events found for this patient.")
        return

    for event in events:
        date = event.get("event_date", "Unknown Date")
        event_type = event.get("event_type", "Medical Event")
        desc = event.get("description", "No description provided.")
        metrics = event.get("metrics", {})
        source = event.get("source_file", "Unknown source")

        with st.expander(f"**{date}** — {event_type}", expanded=True):
            st.markdown(f"*{desc}*")
            
            if metrics:
                st.markdown("**Extracted Metrics:**")
                
                # BUG FIX: If the database accidentally returns a string, safely convert it back to a dictionary
                if isinstance(metrics, str):
                    try:
                        metrics = ast.literal_eval(metrics)
                    except:
                        metrics = {"Data": metrics}
                
                # Only iterate if it successfully parsed as a dictionary
                if isinstance(metrics, dict):
                    cols = st.columns(len(metrics) if len(metrics) < 5 else 4)
                    
                    col_idx = 0
                    for key, value in metrics.items():
                        clean_key = key.replace("_", " ").title()
                        
                        if isinstance(value, (list, dict)):
                            display_value = ", ".join(value) if isinstance(value, list) else str(value)
                        else:
                            display_value = str(value)
                            
                        cols[col_idx % len(cols)].metric(label=clean_key, value=display_value)
                        col_idx += 1
            
            st.caption(f"Source Document: {source}")