#Define Langgraph TypedDict State

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.tools.retriever import create_retriever_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
reviewer_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    structured_data: dict
    context: str
    clinical_brief: str
    guardrail_passed: bool

retirever_tool = create_retriever_tool(
    #retriever,
    name="patient_history_search",
    description = "Use this tool to search and retrieve the patient's medical history, past diagnoses, lab results and general health records.",
)