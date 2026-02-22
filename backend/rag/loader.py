import os
import hashlib
import logging
from typing import List
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Setup basic logging for the loader
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentLoader:
    """Handles loading and splitting of documents from a directory with robust error recovery."""
    
    def __init__(self, data_dir: str = "/data"):
        self.data_dir = data_dir
        # Using RecursiveCharacterTextSplitter for optimal RAG chunking
        # Chunks of 10000 characters with 10% overlap is standard for Gemini-based RAG
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=1000,
            separators=["\n\n", "\n", " ", ""]
        )

    def generate_id(self, doc: Document) -> str:
        """Generates a deterministic ID for a document chunk based on its content and source."""
        content = doc.page_content
        source = doc.metadata.get("source", "unknown")
        # Combine content and source for a unique fingerprint
        fingerprint = f"{content}|{source}"
        return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()

    def load_and_split(self) -> List[Document]:
        """Loads all supported files from data_dir and splits them into chunks."""
        documents = []
        
        if not os.path.exists(self.data_dir):
            logger.warning(f"Data directory {self.data_dir} not found. Attempting to create it.")
            try:
                os.makedirs(self.data_dir, exist_ok=True)
            except Exception as e:
                logger.error(f"Critical failure: Could not create data directory {self.data_dir}: {e}")
                return []

        try:
            files_in_dir = os.listdir(self.data_dir)
        except Exception as e:
            logger.error(f"Failed to list files in {self.data_dir}: {e}")
            return []

        for filename in files_in_dir:
            file_path = os.path.join(self.data_dir, filename)
            
            # Skip non-files and hidden files
            if not os.path.isfile(file_path) or filename.startswith('.'):
                continue
                
            try:
                loader = None
                file_ext = filename.lower()
                
                # Dynamic loader selection based on file extension
                if file_ext.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    loaded_docs = loader.load()
                elif file_ext.endswith(".csv"):
                    # For CSV, we'll implement a more balanced approach to avoid 1-chunk-per-row
                    import csv
                    with open(file_path, newline='', encoding='utf-8', errors='replace') as csvfile:
                        reader = csv.DictReader(csvfile)
                        content_list = []
                        # Group rows together to reduce document count
                        for i, row in enumerate(reader):
                            row_str = ", ".join([f"{k}: {v}" for k, v in row.items()])
                            content_list.append(row_str)
                            
                        # Join every 50 rows into a single document to reduce RAG overhead
                        rows_per_doc = 50
                        loaded_docs = []
                        for i in range(0, len(content_list), rows_per_doc):
                            chunk_content = "\n".join(content_list[i:i + rows_per_doc])
                            loaded_docs.append(Document(
                                page_content=chunk_content,
                                metadata={"source": file_path, "row_range": f"{i}-{i+rows_per_doc}"}
                            ))
                elif file_ext.endswith(".txt") or file_ext.endswith(".md"):
                    # Attempt to load with UTF-8, fallback to Latin-1 if it fails (graceful handling)
                    try:
                        loader = TextLoader(file_path, encoding='utf-8')
                        loaded_docs = loader.load()
                    except (UnicodeDecodeError, Exception):
                        loader = TextLoader(file_path, encoding='latin-1')
                        loaded_docs = loader.load()
                elif file_ext.endswith(".docx"):
                    loader = Docx2txtLoader(file_path)
                    loaded_docs = loader.load()
                else:
                    logger.debug(f"Skipping unsupported file format: {filename}")
                    continue
                
                if loaded_docs:
                    # Ensure absolute path in metadata for consistency
                    for doc in loaded_docs:
                        doc.metadata["source"] = os.path.abspath(file_path)
                    documents.extend(loaded_docs)
                    logger.info(f"Successfully processed: {filename} (Documents: {len(loaded_docs)})")
                    
            except Exception as e:
                logger.error(f"Error loading file {filename}: {str(e)}")
                continue

        if not documents:
            logger.info("No valid document content found in the data folder.")
            return []

        # Perform the actual text splitting for the vector store
        try:
            # For PDF/TXT we still split, for CSV we've already roughly grouped
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Successfully split knowledge base into {len(chunks)} contextual chunks.")
            return chunks
        except Exception as e:
            logger.error(f"Error during document chunking process: {e}")
            return []