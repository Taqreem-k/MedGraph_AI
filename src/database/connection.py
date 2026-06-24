#SQLite or Vector DB initialization

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLm-L6-v2")