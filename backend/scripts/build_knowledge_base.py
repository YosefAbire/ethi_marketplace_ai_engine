import os
import sys
from dotenv import load_dotenv

# Add the parent directory to sys.path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.rag_agent import RAGAgent

def run_sync():
    """
    Manually triggers the document loading, splitting, and embedding process.
    Run this script whenever you add new documents to the /data folder.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("Error: API_KEY not found in environment. Please check your .env file.")
        return

    print("--- Ethi Marketplace: Knowledge Base Build Script ---")
    print("This script will index new or changed documents into the vector store.")
    print("Note: This process uses Gemini Embedding API quota.")
    print("----------------------------------------------------\n")

    # We explicitly EXCLUDE DISABLE_RAG_SYNC for this script to work
    os.environ["DISABLE_RAG_SYNC"] = "false"
    
    try:
        # Initialize the agent
        # The agent __init__ now only loads the existing store (if any)
        agent = RAGAgent(data_dir="./data", persist_dir="./chroma_db")
        
        # Explicitly trigger the sync
        print("Scanning ./data for documents...")
        agent.sync_local_documents("./data")
        
        print("\nBuild Complete! The vector store is now up to date.")
        print("You can now start the API server normally.")
        
    except Exception as e:
        print(f"\nBuild Failed: {e}")

if __name__ == "__main__":
    run_sync()
