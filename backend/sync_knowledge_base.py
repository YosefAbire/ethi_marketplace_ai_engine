#!/usr/bin/env python3
"""
Script to sync documents from the data directory to the RAG vector store.
This will index all documents including the Marketing PDF.
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from agents.rag_agent import RAGAgent

def main():
    """Sync all documents to the knowledge base."""
    print("🚀 Syncing Knowledge Base")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("❌ Error: API_KEY not found in environment")
        print("Please ensure your .env file has API_KEY set")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Set environment for local embeddings (quota-safe)
    os.environ["EMBEDDING_MODE"] = "local"
    os.environ["DISABLE_RAG_SYNC"] = "false"
    
    try:
        # Initialize RAG agent
        print("\n📦 Initializing RAG Agent...")
        rag_agent = RAGAgent(api_key=api_key, data_dir="./data")
        
        # Check data directory
        data_dir = "./data"
        if not os.path.exists(data_dir):
            print(f"❌ Error: Data directory '{data_dir}' not found")
            return False
        
        # List files to be synced
        files = os.listdir(data_dir)
        print(f"\n📄 Files found in data directory:")
        for file in files:
            print(f"   - {file}")
        
        # Sync documents
        print(f"\n🔄 Syncing documents to vector store...")
        print("   This may take a few minutes for large documents...")
        
        rag_agent.sync_local_documents(data_dir, force=True)
        
        # Get final status
        status = rag_agent.get_system_status()
        print(f"\n✅ Sync complete!")
        print(f"   Indexed chunks: {status['indexed_chunks']}")
        print(f"   Vector store ready: {status['vector_store_exists']}")
        print(f"   QA chain ready: {status['qa_chain_ready']}")
        
        # Test query
        print(f"\n🧪 Testing knowledge base with sample query...")
        response = rag_agent.ask("What marketing strategies are mentioned in the documents?")
        print(f"\n📝 Sample Response:")
        print(f"   {response['answer'][:200]}...")
        print(f"   Sources: {response['sources']}")
        
        print(f"\n🎉 Knowledge base is ready for use!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during sync: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
