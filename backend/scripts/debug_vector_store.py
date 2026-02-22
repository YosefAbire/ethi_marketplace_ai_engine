import os
import sys
from dotenv import load_dotenv

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vector_store import VectorStoreManager
from rag.embedding import EmbeddingManager

def debug_store():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    output_file = "debug_output.txt"
    
    with open(output_file, "w") as f:
        if not api_key:
            f.write("API_KEY missing\n")
            return

        f.write("--- Debugging Vector Store ---\n")
        
        # Init embeddings
        embedding_manager = EmbeddingManager(api_key=api_key)
        embeddings = embedding_manager.get_embeddings()
        
        # Init VS Manager
        vs_manager = VectorStoreManager(persist_dir="./chroma_db", embeddings=embeddings)
        
        if not vs_manager.exists():
            f.write("Vector store not found at ./chroma_db\n")
            return

        vector_store = vs_manager.load_store()
        
        # Get all documents (hacky way for Chroma)
        try:
            # Depending on langchain version, this might vary. 
            # But we can try a broad search or peek.
            # Access the underlying client client if possible, but let's just do a similarity search for "Male" or "Female" 
            # which are likely in Mall_Customers.csv
            
            f.write("Querying for Mall_Customers.csv chunks...\n")
            
            # specific file path
            target_file = "Mall_Customers.csv"
            # We need to guess the path used during indexing. 
            # The loader uses os.path.abspath(file_path).
            # Let's try to construct it.
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")
            abs_path = os.path.abspath(os.path.join(data_dir, target_file))
            
            f.write(f"Checking for source: {abs_path}\n")
            
            collection = vector_store._collection
            # Try exact match first
            results = collection.get(where={"source": abs_path}, limit=5)
            
            count = len(results['ids']) if results and 'ids' in results else 0
            
            if count > 0:
                f.write(f"\nSUCCESS: Found {count} chunks for Mall_Customers.csv in the index.\n")
                doc_snippet = results['documents'][0][:100].replace('\n', ' ')
                f.write(f"Sample content: {doc_snippet}...\n")
            else:
                f.write(f"\nExact match failed. Fetching sample to verify paths stored...\n")
                # Fallback: fetch random 10 and print sources
                sample = collection.get(limit=10)
                f.write("Sample sources in DB:\n")
                for meta in sample['metadatas']:
                    f.write(f"- {meta.get('source', 'unknown')}\n")
                 
        except Exception as e:
            f.write(f"Error inspecting store: {e}\n")
    print(f"Debug output written to {output_file}")

if __name__ == "__main__":
    debug_store()
