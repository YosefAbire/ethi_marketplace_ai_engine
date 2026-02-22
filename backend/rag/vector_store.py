import os
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma

class VectorStoreManager:
    """Manages the Chroma vector store lifecycle."""
    
    def __init__(self, persist_dir: str = "./chroma_db", embeddings=None):
        self.persist_dir = persist_dir
        self.embeddings = embeddings

    def exists(self) -> bool:
        """Checks if the vector store already exists on disk."""
        return os.path.exists(self.persist_dir) and len(os.listdir(self.persist_dir)) > 0

    def create_store(self, documents, ids=None):
        """Creates and persists a new vector store from documents."""
        print(f"Creating new vector store at {self.persist_dir}...")
        return Chroma.from_documents(
            documents=documents,
            ids=ids,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )

    def load_store(self):
        """Loads an existing vector store from disk."""
        print(f"Loading existing vector store from {self.persist_dir}...")
        return Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )

    def add_to_store(self, vector_store, documents, ids=None):
        """Adds new documents to an existing persistent vector store."""
        if not documents:
            return vector_store
        print(f"Adding {len(documents)} new chunks to the vector store...")
        vector_store.add_documents(documents=documents, ids=ids)
        return vector_store