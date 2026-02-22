"""
Cloud embeddings implementation using Google Gemini API.
This module handles API quota management and graceful failure handling.
"""

import os
import time
import logging
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings

logger = logging.getLogger(__name__)

class CloudEmbeddings:
    """
    Cloud embeddings using Google Gemini API with robust quota management.
    Includes automatic retry logic and quota exhaustion detection.
    """
    
    def __init__(self, api_key: str = None, batch_size: int = 50, delay_seconds: float = 1.0):
        """
        Initialize cloud embeddings with rate limiting.
        
        Args:
            api_key: Google API key
            batch_size: Number of documents to process per batch (reduced for quota safety)
            delay_seconds: Delay between batches
        """
        self.api_key = api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("Google API Key is required for cloud embeddings.")
        
        self.batch_size = batch_size
        self.delay_seconds = delay_seconds
        
        # Initialize the base embeddings
        self.base_embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=self.api_key
        )
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed documents with quota-safe batching and retry logic.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            QuotaExhaustedException: When daily quota is exceeded
            Exception: For other API errors
        """
        if not texts:
            return []
        
        all_embeddings = []
        total_batches = (len(texts) - 1) // self.batch_size + 1
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            
            logger.info(f"Embedding cloud batch {batch_num}/{total_batches} ({len(batch)} documents)...")
            
            try:
                embeddings = self._embed_batch_with_retry(batch)
                all_embeddings.extend(embeddings)
                
                # Add delay between batches (except the last one)
                if i + self.batch_size < len(texts):
                    time.sleep(self.delay_seconds)
                    
            except QuotaExhaustedException:
                logger.error("Daily quota exhausted during cloud embedding")
                raise
            except Exception as e:
                logger.error(f"Failed to embed batch {batch_num}: {e}")
                raise
        
        logger.info(f"Successfully embedded {len(texts)} documents using cloud API")
        return all_embeddings
    
    def _embed_batch_with_retry(self, batch: List[str], max_retries: int = 3) -> List[List[float]]:
        """
        Embed a single batch with retry logic.
        
        Args:
            batch: List of texts to embed
            max_retries: Maximum number of retry attempts
            
        Returns:
            List of embeddings for the batch
        """
        for attempt in range(max_retries + 1):
            try:
                embeddings = self.base_embeddings.embed_documents(batch)
                return embeddings
                
            except Exception as e:
                error_msg = str(e).lower()
                
                # Check for quota exhaustion
                if "quota" in error_msg or "resource_exhausted" in error_msg or "429" in error_msg:
                    if "daily" in error_msg or "1000" in error_msg:
                        raise QuotaExhaustedException("Daily embedding quota exhausted")
                    
                    # Rate limit - wait and retry
                    if attempt < max_retries:
                        wait_time = (2 ** attempt) * 5  # Exponential backoff: 5s, 10s, 20s
                        logger.warning(f"Rate limited, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                        time.sleep(wait_time)
                        continue
                
                # Other errors - don't retry
                logger.error(f"Cloud embedding error: {e}")
                raise
        
        raise Exception(f"Failed to embed batch after {max_retries} retries")
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query with error handling.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector
        """
        try:
            return self.base_embeddings.embed_query(text)
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "resource_exhausted" in error_msg:
                raise QuotaExhaustedException("Query embedding quota exhausted")
            raise


class QuotaExhaustedException(Exception):
    """Exception raised when API quota is exhausted."""
    pass