"""
Embedding router that intelligently chooses between local and cloud embeddings
based on document count, configuration, and quota status.
"""

import os
import logging
from typing import List, Optional
from .local_embeddings import LocalEmbeddings
from .cloud_embeddings import CloudEmbeddings, QuotaExhaustedException

logger = logging.getLogger(__name__)

class EmbeddingRouter:
    """
    Smart routing system that chooses the optimal embedding strategy
    based on document count, configuration, and API quota status.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the embedding router.
        
        Args:
            api_key: Google API key for cloud embeddings (optional)
        """
        self.api_key = api_key or os.getenv("API_KEY")
        
        # Configuration from environment variables
        self.embedding_mode = os.getenv("EMBEDDING_MODE", "hybrid").lower()
        self.cloud_threshold = int(os.getenv("EMBEDDING_CLOUD_THRESHOLD", "50"))
        
        # Initialize embedding providers
        self.local_embeddings = None
        self.cloud_embeddings = None
        self.quota_exhausted = False
        
        # Validate configuration
        if self.embedding_mode not in ["local", "cloud", "hybrid"]:
            logger.warning(f"Invalid EMBEDDING_MODE '{self.embedding_mode}', defaulting to 'hybrid'")
            self.embedding_mode = "hybrid"
        
        logger.info(f"Embedding router initialized: mode={self.embedding_mode}, threshold={self.cloud_threshold}")
    
    def _get_local_embeddings(self) -> LocalEmbeddings:
        """Lazy initialization of local embeddings."""
        if self.local_embeddings is None:
            try:
                self.local_embeddings = LocalEmbeddings()
                logger.info("Local embeddings initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize local embeddings: {e}")
                raise Exception("Local embeddings unavailable. Please install sentence-transformers: pip install sentence-transformers")
        return self.local_embeddings
    
    def _get_cloud_embeddings(self) -> CloudEmbeddings:
        """Lazy initialization of cloud embeddings."""
        if self.cloud_embeddings is None:
            if not self.api_key:
                raise Exception("API_KEY required for cloud embeddings")
            try:
                self.cloud_embeddings = CloudEmbeddings(self.api_key)
                logger.info("Cloud embeddings initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize cloud embeddings: {e}")
                raise
        return self.cloud_embeddings
    
    def _choose_embedding_strategy(self, document_count: int) -> str:
        """
        Choose the optimal embedding strategy based on configuration and document count.
        
        Args:
            document_count: Number of documents to embed
            
        Returns:
            Strategy name: "local" or "cloud"
        """
        # Force local if quota is exhausted
        if self.quota_exhausted:
            logger.info("Using local embeddings due to quota exhaustion")
            return "local"
        
        # Respect explicit mode settings
        if self.embedding_mode == "local":
            return "local"
        elif self.embedding_mode == "cloud":
            return "cloud"
        
        # Hybrid mode: use threshold to decide
        if document_count > self.cloud_threshold:
            logger.info(f"Using local embeddings for {document_count} documents (> threshold {self.cloud_threshold})")
            return "local"
        else:
            logger.info(f"Using cloud embeddings for {document_count} documents (<= threshold {self.cloud_threshold})")
            return "cloud"
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed documents using the optimal strategy.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        document_count = len(texts)
        strategy = self._choose_embedding_strategy(document_count)
        
        try:
            if strategy == "local":
                embeddings_provider = self._get_local_embeddings()
                return embeddings_provider.embed_documents(texts)
            else:  # cloud
                embeddings_provider = self._get_cloud_embeddings()
                return embeddings_provider.embed_documents(texts)
                
        except QuotaExhaustedException:
            logger.warning("Cloud quota exhausted, falling back to local embeddings")
            self.quota_exhausted = True
            
            # Fallback to local embeddings
            if strategy == "cloud":
                local_embeddings = self._get_local_embeddings()
                return local_embeddings.embed_documents(texts)
            else:
                raise  # Already using local, re-raise the exception
                
        except Exception as e:
            logger.error(f"Embedding failed with strategy '{strategy}': {e}")
            
            # Try fallback if we were using cloud
            if strategy == "cloud" and not self.quota_exhausted:
                logger.info("Attempting fallback to local embeddings")
                try:
                    local_embeddings = self._get_local_embeddings()
                    return local_embeddings.embed_documents(texts)
                except Exception as fallback_error:
                    logger.error(f"Fallback to local embeddings also failed: {fallback_error}")
            
            raise Exception(f"All embedding strategies failed. Last error: {e}")
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query string.
        For queries, we prefer cloud embeddings for consistency with training data,
        but fall back to local if quota is exhausted.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector
        """
        # For queries, prefer cloud unless explicitly set to local or quota exhausted
        if self.embedding_mode == "local" or self.quota_exhausted:
            strategy = "local"
        else:
            strategy = "cloud"
        
        try:
            if strategy == "local":
                embeddings_provider = self._get_local_embeddings()
                return embeddings_provider.embed_query(text)
            else:  # cloud
                embeddings_provider = self._get_cloud_embeddings()
                return embeddings_provider.embed_query(text)
                
        except QuotaExhaustedException:
            logger.warning("Cloud quota exhausted during query, falling back to local")
            self.quota_exhausted = True
            
            if strategy == "cloud":
                local_embeddings = self._get_local_embeddings()
                return local_embeddings.embed_query(text)
            else:
                raise
                
        except Exception as e:
            logger.error(f"Query embedding failed with strategy '{strategy}': {e}")
            
            # Try fallback for cloud queries
            if strategy == "cloud" and not self.quota_exhausted:
                try:
                    local_embeddings = self._get_local_embeddings()
                    return local_embeddings.embed_query(text)
                except Exception as fallback_error:
                    logger.error(f"Query fallback to local embeddings failed: {fallback_error}")
            
            raise Exception(f"Query embedding failed: {e}")
    
    def get_status(self) -> dict:
        """
        Get the current status of the embedding router.
        
        Returns:
            Dictionary with router status information
        """
        return {
            "mode": self.embedding_mode,
            "cloud_threshold": self.cloud_threshold,
            "quota_exhausted": self.quota_exhausted,
            "local_available": self.local_embeddings is not None,
            "cloud_available": self.cloud_embeddings is not None and self.api_key is not None
        }