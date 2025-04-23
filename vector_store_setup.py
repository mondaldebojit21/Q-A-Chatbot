# vector_store_setup.py

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import chromadb

# Load documents from local directory
documents = SimpleDirectoryReader(input_dir="./demo_bot_data/", required_exts=[".md"], recursive=True).load_data()

# Define embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.embed_model = embed_model

# Setup ChromaDB persistent client
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("Ubuntu_Vector_DB")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Storage Context
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create and persist vector index
index = VectorStoreIndex.from_documents(
    documents, 
    storage_context=storage_context,
    embed_model=embed_model,
    show_progress=True
)

print("✅ Vector store created and stored in ./chroma_db")
