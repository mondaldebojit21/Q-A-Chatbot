from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.google_genai import GoogleGenAI
import chromadb

# Initialize LLM and embedding
llm = GoogleGenAI(model="gemini-2.0-flash")
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

Settings.llm = llm
Settings.embed_model = embed_model

# Load ChromaDB from disk
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("Ubuntu_Vector_DB")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Load vector index from vector store
index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model, show_progress=True)

# Build query engine
query_engine = index.as_query_engine()

# Sample query
query = "Tell me about Ubuntu SSO accounts"
response = query_engine.query(query)

print("Query:", query)
print("Response:", response)
