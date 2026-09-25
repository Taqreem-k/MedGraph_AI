import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables to ensure GOOGLE_API_KEY is available
load_dotenv()

# Fail fast if the API key is missing
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")

# Initialize the Gemini embedding model
# text-embedding-004 is currently the standard for Google GenAI embeddings
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def build_local_vector_store(text_chunks: List[str]) -> Optional[FAISS]:
    if not text_chunks:
        return None
    
    # Convert text chunks into vectors and store them in the FAISS index
    vector_store = FAISS.from_texts(text_chunks, embeddings_model)
    return vector_store

def search_similar_records(vector_store: FAISS, query: str, top_k: int = 3) -> List[str]:
    if not vector_store:
        return []
        
    # Retrieve the top_k most semantically similar documents
    docs = vector_store.similarity_search(query, k=top_k)
    
    # Extract the raw string content from the LangChain Document objects
    return [doc.page_content for doc in docs]