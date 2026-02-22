"""
Rebuild the knowledge base with the production RAG system.
This will re-index all documents using local embeddings.
"""
import os
import shutil
import sys
from pathlib import Path
from dotenv import load_dotenv

# Change to backend directory
backend_dir = Path(__file__).parent
os.chdir(backend_dir)

# Load environment
load_dotenv()

# Configure for local embeddings (quota-safe)
os.environ["EMBEDDING_MODE"] = "local"
os.environ["DISABLE_RAG_SYNC"] = "false"

print("🔄 Rebuilding Knowledge Base with Production RAG System")
print("=" * 60)

# Remove old vector store
chroma_dir = "./chroma_db"
if os.path.exists(chroma_dir):
    print(f"\n🗑️  Removing old vector store at {chroma_dir}...")
    shutil.rmtree(chroma_dir)
    print("✅ Old vector store removed")

# Initialize new RAG agent
print("\n📦 Initializing Production RAG Agent...")
from agents.rag_agent import RAGAgent

rag_agent = RAGAgent(data_dir="./data", persist_dir="./chroma_db")
print("✅ RAG Agent initialized")

# List files
data_dir = "./data"
files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
print(f"\n📄 Files to index:")
for f in files:
    print(f"   - {f}")

# Sync documents
print(f"\n🔄 Indexing documents (using local embeddings)...")
print("   This will take a few minutes...")

rag_agent.sync_local_documents(data_dir, force=True)

# Get status
status = rag_agent.get_system_status()
print(f"\n✅ Knowledge Base Ready!")
print(f"   Indexed chunks: {status['indexed_chunks']}")
print(f"   Embedding mode: {status['embedding_system']['router']['mode']}")

# Test with Marketing PDF query
print(f"\n🧪 Testing with Marketing PDF query...")
result = rag_agent.ask("List 5 marketing strategies from the Marketing PDF")
print(f"\n📝 Response:")
print(f"{result['answer']}")
print(f"\n📚 Sources: {', '.join(result['sources'])}")

print(f"\n🎉 Knowledge base rebuild complete!")
