from typing import TypedDict, List, Dict, Any, Annotated
import operator

class MedGraphState(TypedDict):
    # File metadata
    file_name: str
    mime_type: str
    
    # The raw input generated from Day 1 (e.g., base64 strings or OCR text)
    raw_data: List[Dict[str, str]] 
    
    # The intermediate extraction layer
    extracted_text: str
    
    # The final structured output for the ChronoHealth timeline
    # operator.add allows nodes to append items to the list instead of overwriting it
    timeline_events: Annotated[List[Dict[str, Any]], operator.add]
    
    # Workflow routing and error tracking
    status: str
    errors: Annotated[List[str], operator.add]