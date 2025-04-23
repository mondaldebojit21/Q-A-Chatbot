from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.google_genai import GoogleGenAI
import chromadb

class Query(BaseModel):
    question: str

app = FastAPI(title="Ubuntu Chatbot API")

# Init
llm = GoogleGenAI(model="gemini-2.0-flash")
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

Settings.llm = llm
Settings.embed_model = embed_model

# Load ChromaDB
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("Ubuntu_Vector_DB")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model, show_progress=False)

@app.post("/ask")
async def ask_question(query: Query):
    try:
        engine = index.as_query_engine()
        answer = engine.query(query.question)
        return {"question": query.question, "answer": str(answer)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
