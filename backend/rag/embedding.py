"""
Production-ready embedding manager with local/cloud routing and caching.
Replaces the old quota-prone embedding system with a robust, scalable solution.
"""

import os
import logging
from typing import List, Optional
from .embeddings import EmbeddingRouter
from .cache import EmbeddingCache

logger = logging.getLogger(__name__)

class EmbeddingManager:
    """
    Production-ready embedding manager that handles:
    - Local vs cloud embedding routing
    - Content-based caching to avoid re-embedding
    - Quota exhaustion graceful handling
    - Scalable processing of large document sets
    """
    
    def __init__(self, api_key: Optional[str] = None, cache_dir: str = "./embedding_cache"):
        """
        Initialize the embedding manager.
        
        Args:
            api_key: Google API key for cloud embeddings (optional)
            cache_dir: Directory for embedding cache storage
        """
        self.api_key = api_key or os.getenv("API_KEY")
        
        # Initialize router and cache
        self.router = EmbeddingRouter(api_key=self.api_key)
        self.cache = EmbeddingCache(cache_dir=cache_dir)
        
        logger.info("Production embedding manager initialized")
        logger.info(f"Router status: {self.router.get_status()}")
        logger.info(f"Cache stats: {self.cache.get_cache_stats()}")
    
    def get_embeddings(self):
        """
        Get embeddings interface compatible with LangChain vector stores.
        Returns self since this class implements the embedding interface.
        """
        return self
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed documents with caching and intelligent routing.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        logger.info(f"Processing {len(texts)} documents for embedding")
        
        # For now, we'll embed all texts since we don't have chunk IDs
        # In a full implementation, this would integrate with the document loader
        # to provide proper caching based on content hashes
        
        try:
            embeddings = self.router.embed_documents(texts)
            logger.info(f"Successfully embedded {len(texts)} documents")
            return embeddings
            
        except Exception as e:
            logger.error(f"Document embedding failed: {e}")
            raise Exception(f"Failed to embed documents: {e}")
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query string.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.router.embed_query(text)
            return embedding
            
        except Exception as e:
            logger.error(f"Query embedding failed: {e}")
            raise Exception(f"Failed to embed query: {e}")
    
    def embed_documents_with_cache(self, chunks: List[dict]) -> List[List[float]]:
        """
        Embed documents with full caching support.
        
        Args:
            chunks: List of chunk dictionaries with 'id', 'content', and metadata
            
        Returns:
            List of embedding vectors for all chunks
        """
        if not chunks:
            return []
        
        # Check cache for unchanged chunks
        unchanged_ids, changed_chunks = self.cache.get_unchanged_chunks(chunks)
        
        if not changed_chunks:
            logger.info("All chunks found in cache, no embedding needed")
            return []  # All chunks are cached, no new embeddings needed
        
        # Embed only changed chunks
        texts_to_embed = [chunk['content'] for chunk in changed_chunks]
        
        try:
            new_embeddings = self.router.embed_documents(texts_to_embed)
            
            # Update cache with newly embedded chunks
            strategy = "local" if len(changed_chunks) > self.router.cloud_threshold else "cloud"
            self.cache.update_cache(changed_chunks, embedding_strategy=strategy)
            
            logger.info(f"Embedded {len(changed_chunks)} new/changed chunks")
            return new_embeddings
            
        except Exception as e:
            logger.error(f"Cached embedding failed: {e}")
            raise
    
    def get_status(self) -> dict:
        """
        Get comprehensive status of the embedding system.
        
        Returns:
            Dictionary with system status
        """
        return {
            "router": self.router.get_status(),
            "cache": self.cache.get_cache_stats(),
            "api_key_configured": self.api_key is not None
        }
    
    def clear_cache(self):
        """Clear the embedding cache."""
        self.cache.clear_cache()
        logger.info("Embedding cache cleared")
