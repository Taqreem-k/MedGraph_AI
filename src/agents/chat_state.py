from typing import TypedDict, List

class ClinicalChatState(TypedDict):
    patient_name: str
    user_query: str
    retrieved_context: List[str]
    draft_response: str
    final_response: str
    compliance_status: str  
    guardrail_reasoning: str 