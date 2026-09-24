import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")

# Initialize the primary Vision-capable Gemini model.
# Temperature is set to 0.0 to maximize determinism and minimize hallucinations 
primary_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  
    temperature=0.0,
    max_tokens=4096
)

# fast_router_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0.0)