
import os
from dotenv import load_dotenv
from agents.rag_agent import RAGAgent

# Load environment variables from .env file
load_dotenv()


def run_test():
    # Ensure you have your API_KEY set in the environment
    # os.environ["API_KEY"] = "your-api-key-here"
    
    print("--- Testing Ethi Marketplace RAG Agent ---")
    
    try:
        # Enable sync for testing
        os.environ["DISABLE_RAG_SYNC"] = "false"
        
        # Initialize the agent
        agent = RAGAgent(data_dir="./data", persist_dir="./chroma_db")
        
        # Manually trigger sync for test if needed
        agent.sync_local_documents("./data")
        
        query = "What are the marketplace policies for selling grain?"
        print(f"Query: {query}")
        
        response = agent.ask(query)
        print("\nStructured Response:")
        print(f"Answer: {response.get('answer')}")
        print(f"Sources: {response.get('sources')}")
        print(f"Confidence: {response.get('confidence')}")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    # Create sample data directory for testing if it doesn't exist
    if not os.path.exists("./data"):
        os.makedirs("./data")
        with open("./data/sample.txt", "w") as f:
            f.write("Ethi Marketplace Grain Policy: All grains must be dried to 12% moisture. Teff requires specialized packaging.")
            
    run_test()
