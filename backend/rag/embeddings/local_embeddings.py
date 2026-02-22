"""
Local embeddings implementation using sentence-transformers.
This module provides offline embedding capabilities to avoid API quota issues.
"""

import os
import logging
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class LocalEmbeddings:
    """
    Local embeddings using sentence-transformers.
    Runs completely offline with no API dependencies.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize local embeddings with a lightweight, high-quality model.
        
        Args:
            model_name: HuggingFace model name. Default is all-MiniLM-L6-v2 (22MB, fast, good quality)
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model with error handling."""
        try:
            logger.info(f"Loading local embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Successfully loaded local embedding model")
        except Exception as e:
            logger.error(f"Failed to load local embedding model: {e}")
            # Fallback to a smaller model if the primary fails
            try:
                fallback_model = "all-MiniLM-L6-v2"
                logger.info(f"Attempting fallback to: {fallback_model}")
                self.model = SentenceTransformer(fallback_model)
                logger.info(f"Successfully loaded fallback embedding model")
            except Exception as fallback_error:
                logger.error(f"Failed to load fallback model: {fallback_error}")
                raise Exception("Could not load any local embedding model. Please check your internet connection for initial model download.")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents using local model.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (as lists of floats)
        """
        if not self.model:
            raise Exception("Local embedding model not loaded")
        
        if not texts:
            return []
        
        try:
            logger.info(f"Embedding {len(texts)} documents locally...")
            # Encode all texts at once for efficiency
            embeddings = self.model.encode(texts, convert_to_tensor=False, show_progress_bar=True)
            
            # Convert numpy arrays to lists for compatibility with vector stores
            if isinstance(embeddings, np.ndarray):
                embeddings = embeddings.tolist()
            
            logger.info(f"Successfully embedded {len(texts)} documents locally")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error during local embedding: {e}")
            raise Exception(f"Local embedding failed: {e}")
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query string.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        if not self.model:
            raise Exception("Local embedding model not loaded")
        
        try:
            embedding = self.model.encode([text], convert_to_tensor=False)[0]
            
            # Convert numpy array to list
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()
                
            return embedding
            
        except Exception as e:
            logger.error(f"Error during local query embedding: {e}")
            raise Exception(f"Local query embedding failed: {e}")
    
    def get_dimension(self) -> int:
        """Get the dimension of the embedding vectors."""
        if not self.model:
            return 384  # Default dimension for all-MiniLM-L6-v2
        return self.model.get_sentence_embedding_dimension()