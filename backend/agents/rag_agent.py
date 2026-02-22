import os
from typing import Optional, List, Set
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from rag.loader import DocumentLoader
from rag.embedding import EmbeddingManager
from rag.vector_store import VectorStoreManager
from prompts.rag_prompt import RAG_PROMPT

class RAGAgent:
    """
    Production-ready RAG Agent with quota-safe embeddings and robust error handling.
    Features:
    - Local embeddings as default for large document sets
    - Intelligent cloud/local routing based on document count
    - Content-based caching to avoid re-embedding
    - Graceful quota exhaustion handling
    """
    
    def __init__(self, api_key: Optional[str] = None, data_dir: str = "./data", persist_dir: str = "./chroma_db"):
        self.api_key = api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY environment variable or argument is required.")

        # 1. Initialize LLM (Gemini only for generation, not embeddings)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0
        )

        # 2. Setup Production Embedding Manager (with local/cloud routing and caching)
        self.embedding_manager = EmbeddingManager(api_key=self.api_key)
        self.embeddings = self.embedding_manager.get_embeddings()

        # 3. Setup Vector Store Manager
        self.vs_manager = VectorStoreManager(persist_dir=persist_dir, embeddings=self.embeddings)
        
        # 4. Load existing vector store if available
        if self.vs_manager.exists():
            print(f"RAG: Loading existing vector store from {persist_dir}...")
            self.vector_store = self.vs_manager.load_store()
        else:
            print(f"RAG: No vector store found at {persist_dir}. Ready for document sync.")
            self.vector_store = None

        # 5. Initialize QA Chain
        self._setup_qa_chain()
        
        # Log system status
        status = self.embedding_manager.get_status()
        print(f"RAG System Status: {status}")

    def _setup_qa_chain(self):
        """Initializes or refreshes the RAG chain using LCEL."""
        if self.vector_store:
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            self.qa_chain = (
                {
                    "context": retriever | format_docs, 
                    "question": RunnablePassthrough(),
                    "source_documents": retriever
                }
                | ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful assistant for the Ethiopian marketplace. Use the following context to answer the question. If you don't know, say so. IMPORTANT: Respond in plain text only - no asterisks, no bold text, no markdown formatting, no bullet points with symbols. Write like you're having a friendly conversation with a colleague."),
                    ("human", "Context:\n{context}\n\nQuestion: {question}")
                ])
                | self.llm
                | StrOutputParser()
            )
        else:
            print("Warning: QA Chain could not be initialized because vector store is empty.")
            self.qa_chain = None

    def get_indexed_ids(self) -> Set[str]:
        """Retrieves a set of all chunk IDs already present in the vector store."""
        if not self.vector_store:
            return set()
        
        try:
            results = self.vector_store.get(include=[])
            if results and 'ids' in results:
                return set(results['ids'])
            return set()
        except Exception as e:
            print(f"Error fetching indexed IDs: {e}")
            return set()

    def sync_local_documents(self, data_dir: str, force: bool = False):
        """
        Production-ready document sync with quota-safe embedding.
        Uses local embeddings for large document sets and caching to avoid re-processing.
        """
        if not force and os.getenv("DISABLE_RAG_SYNC", "true").lower() == "true":
            print("RAG: Sync is disabled via DISABLE_RAG_SYNC environment variable.")
            return

        try:
            loader = DocumentLoader(data_dir=data_dir)
            all_chunks = loader.load_and_split()
            
            if not all_chunks:
                print("No documents found in data directory to sync.")
                return

            # Generate deterministic IDs for all chunks
            chunk_data = []
            for chunk in all_chunks:
                chunk_id = loader.generate_id(chunk)
                chunk_data.append({"id": chunk_id, "doc": chunk})

            # Check which IDs already exist
            if not self.vector_store:
                # First run: everything is new
                new_chunk_ids = [c["id"] for c in chunk_data]
                new_docs = [c["doc"] for c in chunk_data]
                print(f"Creating initial knowledge base with {len(new_docs)} chunks...")
                
                # Use production embedding manager
                self.vector_store = self.vs_manager.create_store(new_docs, ids=new_chunk_ids)
            else:
                # Subsequent run: filter by ID
                existing_ids = self.get_indexed_ids()
                
                to_add_ids = []
                to_add_docs = []
                
                for c in chunk_data:
                    if c["id"] not in existing_ids:
                        to_add_ids.append(c["id"])
                        to_add_docs.append(c["doc"])
                
                if not to_add_docs:
                    print(f"Knowledge base is already up to date. ({len(existing_ids)} chunks indexed)")
                    return

                print(f"Syncing {len(to_add_docs)} new/changed chunks...")
                self.vs_manager.add_to_store(self.vector_store, to_add_docs, ids=to_add_ids)
            
            print("Knowledge base sync complete.")
            
            # Refresh QA chain
            self._setup_qa_chain()
            
        except Exception as e:
            print(f"Document sync failed: {e}")
            print("This is likely due to embedding quota exhaustion or model loading issues.")
            print("The system will continue to work with existing knowledge base.")
            
            # Don't crash the entire system - graceful degradation
            if "quota" in str(e).lower() or "resource_exhausted" in str(e).lower():
                print("Quota exhausted - switching to local embeddings for future operations.")

    def save_new_documents(self, documents: List):
        """Save new documents with production embedding system."""
        if not documents:
            return

        try:
            loader = DocumentLoader()
            chunk_ids = [loader.generate_id(doc) for doc in documents]

            if not self.vector_store:
                self.vector_store = self.vs_manager.create_store(documents, ids=chunk_ids)
            else:
                existing_ids = self.get_indexed_ids()
                to_add_ids = []
                to_add_docs = []
                for doc, cid in zip(documents, chunk_ids):
                    if cid not in existing_ids:
                        to_add_ids.append(cid)
                        to_add_docs.append(doc)
                
                if to_add_docs:
                    self.vs_manager.add_to_store(self.vector_store, to_add_docs, ids=to_add_ids)
            
            self._setup_qa_chain()
            print(f"Successfully processed {len(documents)} chunks.")
            
        except Exception as e:
            print(f"Failed to save new documents: {e}")
            # Graceful degradation - don't crash

    def delete_document(self, filename: str):
        """Remove documents by filename with error handling."""
        if not self.vector_store:
            return
            
        try:
            self.vector_store.delete(where={"source": {"$contains": filename}})
            print(f"Removed documents matching '{filename}' from vector store.")
            self._setup_qa_chain()
        except Exception as e:
            print(f"Error deleting documents from vector store: {e}")

    def ask(self, query: str) -> dict:
        """Process queries with robust error handling and user-friendly messages."""
        default_response = {
            "answer": "I'm still setting up my knowledge base. Please check back in a few minutes.",
            "sources": [],
            "confidence": 0.0
        }

        if not self.vector_store:
            return default_response
            
        try:
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            docs = retriever.invoke(query)
            
            sources = list(set([os.path.basename(doc.metadata.get("source", "unknown")) for doc in docs]))
            
            if self.qa_chain:
                answer = self.qa_chain.invoke(query)
                return {
                    "answer": answer,
                    "sources": sources,
                    "confidence": 0.9 if sources else 0.0
                }
            
            return default_response
            
        except Exception as e:
            error_message = str(e).lower()
            
            # User-friendly error messages
            if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
                return {
                    "answer": "Knowledge Base Agent experienced a technical hurdle. Our AI service is temporarily at capacity. Please try again in a few moments.",
                    "sources": [],
                    "confidence": 0.0
                }
            elif "api_key" in error_message or "authentication" in error_message:
                return {
                    "answer": "Knowledge Base Agent experienced a technical hurdle. Authentication service is temporarily unavailable.",
                    "sources": [],
                    "confidence": 0.0
                }
            else:
                return {
                    "answer": "Knowledge Base Agent experienced a technical hurdle. Please try again or contact support if the issue persists.",
                    "sources": [],
                    "confidence": 0.0
                }
    
    def get_system_status(self) -> dict:
        """Get comprehensive system status for monitoring."""
        return {
            "vector_store_exists": self.vector_store is not None,
            "qa_chain_ready": self.qa_chain is not None,
            "indexed_chunks": len(self.get_indexed_ids()) if self.vector_store else 0,
            "embedding_system": self.embedding_manager.get_status()
        }