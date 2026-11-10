import json
from langchain_core.messages import HumanMessage
from src.database import get_timeline_events
from src.utils import build_local_vector_store, search_similar_records
from .llm import primary_llm
from .chat_state import ClinicalChatState
from .prompts import CLINICAL_ASSISTANT_PROMPT, MEDICAL_GUARDRAIL_PROMPT

def retrieval_node(state: ClinicalChatState) -> dict:
    patient_name = state.get("patient_name")
    query = state.get("user_query")
    
    # Fetch verified data from the database
    raw_events = get_timeline_events(patient_name)
    
    if not raw_events:
        return {"retrieved_context": ["No medical records found for this patient."]}

    # Convert the structured database rows into readable text chunks for the embedding model
    text_chunks = []
    for event in raw_events:
        metrics_str = json.dumps(event.get("metrics", {}))
        chunk = (f"Date: {event.get('event_date')} | Type: {event.get('event_type')} | "
                 f"Notes: {event.get('description')} | Metrics: {metrics_str}")
        text_chunks.append(chunk)

    # Build the in-memory vector store and perform the RAG search
    vector_store = build_local_vector_store(text_chunks)
    retrieved_docs = search_similar_records(vector_store, query, top_k=4)

    return {"retrieved_context": retrieved_docs}

def drafter_node(state: ClinicalChatState) -> dict:
    patient_name = state.get("patient_name")
    query = state.get("user_query")
    context = "\n".join(state.get("retrieved_context", []))

    # Format the prompt
    formatted_prompt = CLINICAL_ASSISTANT_PROMPT.format(
        patient_name=patient_name,
        context=context,
        query=query
    )

    response = primary_llm.invoke([HumanMessage(content=formatted_prompt)])
    
    return {"draft_response": response.content}

def guardrail_node(state: ClinicalChatState) -> dict:
    draft = state.get("draft_response")
    context = "\n".join(state.get("retrieved_context", []))

    formatted_prompt = MEDICAL_GUARDRAIL_PROMPT.format(
        context=context,
        draft=draft
    )

    response = primary_llm.invoke([HumanMessage(content=formatted_prompt)])
    eval_text = response.content.strip()

    # Parse the strict formatting requested in the prompt (STATUS and REASONING)
    status = "FAIL"
    reasoning = "Guardrail parsing error."
    
    for line in eval_text.split("\n"):
        if line.startswith("STATUS:"):
            status = line.replace("STATUS:", "").strip()
        elif line.startswith("REASONING:"):
            reasoning = line.replace("REASONING:", "").strip()

    # Determine the final output based on the compliance status
    if status == "PASS":
        final_text = draft
    else:
        final_text = f"**Response Blocked by Medical Guardrail:** {reasoning}"

    return {
        "compliance_status": status,
        "guardrail_reasoning": reasoning,
        "final_response": final_text
    }