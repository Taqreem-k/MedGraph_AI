from langchain_core.messages import HumanMessage, SystemMessage
from .llm import primary_llm
from .prompts import VISION_EXTRACTION_PROMPT
from .state import MedGraphState

def vision_extraction_node(state: MedGraphState) -> dict:
    raw_data = state.get("raw_data", [])
    
    if not raw_data:
        # We append to the errors list using LangGraph's state updater
        return {"status": "failed", "errors": ["No raw data provided for extraction."]}
    
    # 1. Construct the multimodal message payload
    content_list = [{"type": "text", "text": "Extract medical information from the following document pages:"}]
    
    for item in raw_data:
        b64_string = item.get("image_data")
        if b64_string:
            # LangChain standard multimodal format
            content_list.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64_string}"}
            })
            
    # 2. Assemble the final prompt sequence
    messages = [
        SystemMessage(content=VISION_EXTRACTION_PROMPT),
        HumanMessage(content=content_list)
    ]
    
    # 3. Invoke the Gemini Vision model
    try:
        response = primary_llm.invoke(messages)
        
        # We return a dictionary containing ONLY the keys in our State that we want to update
        return {
            "extracted_text": response.content,
            "status": "extraction_complete"
        }
    except Exception as e:
        return {
            "status": "failed",
            "errors": [f"Vision extraction failed: {str(e)}"]
        }