#!/usr/bin/env python3
"""
Test script to verify Marketing PDF queries work correctly.
Run this to confirm the knowledge base is properly indexed.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Change to backend directory
backend_dir = Path(__file__).parent
os.chdir(backend_dir)

# Load environment
load_dotenv()

print("🧪 Testing Marketing PDF Knowledge Base")
print("=" * 60)

# Initialize RAG agent
print("\n📦 Loading RAG Agent...")
from agents.rag_agent import RAGAgent

try:
    rag_agent = RAGAgent(data_dir="./data", persist_dir="./chroma_db")
    
    # Check status
    status = rag_agent.get_system_status()
    print(f"✅ RAG Agent loaded")
    print(f"   Indexed chunks: {status['indexed_chunks']}")
    print(f"   Vector store exists: {status['vector_store_exists']}")
    print(f"   QA chain ready: {status['qa_chain_ready']}")
    
    if not status['vector_store_exists']:
        print("\n❌ Error: Vector store not found!")
        print("   Run: python backend/rebuild_knowledge_base.py")
        sys.exit(1)
    
    if status['indexed_chunks'] == 0:
        print("\n❌ Error: No documents indexed!")
        print("   Run: python backend/rebuild_knowledge_base.py")
        sys.exit(1)
    
    # Test query
    print(f"\n🔍 Testing query: 'List 5 marketing strategies from the Marketing PDF'")
    print("   Processing...")
    
    result = rag_agent.ask("List 5 marketing strategies from the Marketing PDF")
    
    print(f"\n✅ Query successful!")
    print(f"\n📝 Answer:")
    print(f"{result['answer']}")
    print(f"\n📚 Sources: {', '.join(result['sources'])}")
    print(f"🎯 Confidence: {result['confidence']}")
    
    # Additional test
    print(f"\n🔍 Testing another query: 'What is positioning strategy?'")
    result2 = rag_agent.ask("What is positioning strategy according to the Marketing PDF?")
    print(f"\n📝 Answer:")
    print(f"{result2['answer'][:300]}...")
    
    print(f"\n🎉 Knowledge base is working correctly!")
    print(f"\n💡 Next step: Restart your backend server to use this knowledge base")
    print(f"   Command: cd backend && uvicorn api.main:app --reload")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print(f"\n💡 Try rebuilding the knowledge base:")
    print(f"   python backend/rebuild_knowledge_base.py")
    sys.exit(1)
