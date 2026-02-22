#!/usr/bin/env python3
"""
Debug script to see the actual error when querying the RAG agent.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import traceback

# Change to backend directory
backend_dir = Path(__file__).parent
os.chdir(backend_dir)

# Load environment
load_dotenv()

print("🔍 Debugging RAG Query")
print("=" * 60)

from agents.rag_agent import RAGAgent

try:
    print("\n📦 Loading RAG Agent...")
    rag_agent = RAGAgent(data_dir="./data", persist_dir="./chroma_db")
    
    status = rag_agent.get_system_status()
    print(f"✅ Status: {status['indexed_chunks']} chunks, QA ready: {status['qa_chain_ready']}")
    
    print(f"\n🔍 Testing query with full error details...")
    
    # Query directly to see the actual error
    query = "List 5 marketing strategies from the Marketing PDF"
    
    if not rag_agent.vector_store:
        print("❌ No vector store!")
        sys.exit(1)
    
    print("   Step 1: Retrieving documents...")
    retriever = rag_agent.vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    print(f"   ✅ Retrieved {len(docs)} documents")
    
    for i, doc in enumerate(docs):
        print(f"      Doc {i+1}: {doc.metadata.get('source', 'unknown')} ({len(doc.page_content)} chars)")
    
    print("\n   Step 2: Invoking QA chain...")
    if rag_agent.qa_chain:
        try:
            answer = rag_agent.qa_chain.invoke(query)
            print(f"   ✅ Got answer: {answer[:200]}...")
        except Exception as chain_error:
            print(f"   ❌ QA Chain Error: {chain_error}")
            print(f"\n   Full traceback:")
            traceback.print_exc()
    else:
        print("   ❌ QA chain not initialized!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nFull traceback:")
    traceback.print_exc()
