"""
Cache module for the RAG system.
Provides embedding caching to avoid redundant processing.
"""

from .embedding_cache import EmbeddingCache, create_embedding_cache

__all__ = [
    "EmbeddingCache",
    "create_embedding_cache"
]