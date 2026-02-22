"""Quick sync script to index documents into the knowledge base."""
import os
os.environ["EMBEDDING_MODE"] = "local"  # Use local embeddings (quota-safe)
os.environ["DISABLE_RAG_SYNC"] = "false"  # Enable sync

from dotenv import load_dotenv
load_dotenv()

from agents.rag_agent import RAGAgent

print("Initializing RAG Agent...")
rag = RAGAgent(data_dir="./data", persist_dir="./chroma_db")

print("\nSyncing documents...")
rag.sync_local_documents("./data", force=True)

print("\nDone! Testing query...")
result = rag.ask("What are the marketing strategies?")
print(f"\nAnswer: {result['answer']}")
print(f"Sources: {result['sources']}")
