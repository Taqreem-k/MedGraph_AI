#Define Langgraph TypedDict State

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
reviewer_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    structured_data: dict
    context: str
    clinical_brief: str
    guardrail_passed: bool