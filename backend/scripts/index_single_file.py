import os
import sys
from dotenv import load_dotenv

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.loader import DocumentLoader
from rag.vector_store import VectorStoreManager
from rag.embedding import EmbeddingManager

def index_file(filename):
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("API_KEY missing")
        return

    print(f"--- Indexing Single File: {filename} ---")
    
    # Init embeddings
    embedding_manager = EmbeddingManager(api_key=api_key)
    embeddings = embedding_manager.get_embeddings()
    
    # Init VS Manager
    vs_manager = VectorStoreManager(persist_dir="./chroma_db", embeddings=embeddings)
    
    # Load specific file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    file_path = os.path.join(data_dir, filename)
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Hack: We can use the loader, but we need to trick it or manually call internal methods?
    # Actually, DocumentLoader iterates data_dir.
    # We can create a temporary loader pointing to a temp dir?
    # Or just modify loader to accept a single file? 
    # Or just write custom loading logic here reusing the loader's split logic.
    
    # Easiest: Use loader but filter results?
    # Or better: Just use loader.load_and_split() but move other files out? No.
    
    # Let's instantiate loader and manually process.
    loader = DocumentLoader(data_dir=data_dir)
    
    # Inspect loader code: it iterates listdir.
    # We will manually trigger the specific logic for CSV
    from langchain_core.documents import Document
    import csv

    documents = []
    
    try:
        if filename.endswith(".csv"):
             with open(file_path, newline='', encoding='utf-8', errors='replace') as csvfile:
                reader = csv.DictReader(csvfile)
                content_list = []
                for i, row in enumerate(reader):
                    row_str = ", ".join([f"{k}: {v}" for k, v in row.items()])
                    content_list.append(row_str)
                    
                rows_per_doc = 50
                for i in range(0, len(content_list), rows_per_doc):
                    chunk_content = "\n".join(content_list[i:i + rows_per_doc])
                    documents.append(Document(
                        page_content=chunk_content,
                        metadata={"source": os.path.abspath(file_path), "row_range": f"{i}-{i+rows_per_doc}"}
                    ))
        else:
            print("Only CSV support implemented in this quick script for now.")
            return

        if not documents:
            print("No content loaded.")
            return

        print(f"Loaded {len(documents)} chunks from {filename}.")
        
        # Split? CSV chunks are likely already small enough, but let's run through splitter if needed.
        # But our loader logic for CSV *already* chunks by rows. 
        # The loader.load_and_split() usually calls self.text_splitter.split_documents(documents)
        # Let's do that to be consistent.
        chunks = loader.text_splitter.split_documents(documents)
        
        print(f"Final chunks to index: {len(chunks)}")
        
        # Generate IDs
        ids = [loader.generate_id(doc) for doc in chunks]
        
        # Add to store
        vector_store = vs_manager.load_store()
        if not vector_store:
             print("Creating new store...")
             vector_store = vs_manager.create_store(chunks, ids=ids)
        else:
             print("Adding to existing store...")
             vs_manager.add_to_store(vector_store, chunks, ids=ids)
             
        print("Success! File indexed.")
        
    except Exception as e:
        print(f"Error during indexing: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python index_single_file.py <filename>")
    else:
        index_file(sys.argv[1])
