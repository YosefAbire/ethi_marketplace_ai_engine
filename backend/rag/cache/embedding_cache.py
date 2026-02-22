"""
Embedding cache system to prevent re-embedding of unchanged documents.
Uses content hashing to detect changes and avoid redundant API calls.
"""

import os
import json
import hashlib
import logging
from typing import Dict, List, Set, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class EmbeddingCache:
    """
    Content-based caching system for embeddings.
    Tracks document content hashes to avoid re-embedding unchanged content.
    """
    
    def __init__(self, cache_dir: str = "./embedding_cache"):
        """
        Initialize the embedding cache.
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Cache files
        self.hash_cache_file = self.cache_dir / "content_hashes.json"
        self.metadata_cache_file = self.cache_dir / "embedding_metadata.json"
        
        # In-memory caches
        self.content_hashes: Dict[str, str] = {}  # chunk_id -> content_hash
        self.embedding_metadata: Dict[str, dict] = {}  # chunk_id -> metadata
        
        # Load existing cache
        self._load_cache()
        
        logger.info(f"Embedding cache initialized with {len(self.content_hashes)} cached items")
    
    def _load_cache(self):
        """Load cache data from disk."""
        try:
            if self.hash_cache_file.exists():
                with open(self.hash_cache_file, 'r', encoding='utf-8') as f:
                    self.content_hashes = json.load(f)
            
            if self.metadata_cache_file.exists():
                with open(self.metadata_cache_file, 'r', encoding='utf-8') as f:
                    self.embedding_metadata = json.load(f)
                    
        except Exception as e:
            logger.warning(f"Failed to load embedding cache: {e}")
            self.content_hashes = {}
            self.embedding_metadata = {}
    
    def _save_cache(self):
        """Save cache data to disk."""
        try:
            with open(self.hash_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.content_hashes, f, indent=2)
            
            with open(self.metadata_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.embedding_metadata, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save embedding cache: {e}")
    
    def _compute_content_hash(self, content: str) -> str:
        """
        Compute SHA-256 hash of content for change detection.
        
        Args:
            content: Text content to hash
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def get_unchanged_chunks(self, chunks: List[dict]) -> Tuple[List[str], List[dict]]:
        """
        Identify chunks that haven't changed since last embedding.
        
        Args:
            chunks: List of chunk dictionaries with 'id', 'content', and optional metadata
            
        Returns:
            Tuple of (unchanged_chunk_ids, changed_chunks)
        """
        unchanged_ids = []
        changed_chunks = []
        
        for chunk in chunks:
            chunk_id = chunk['id']
            content = chunk['content']
            current_hash = self._compute_content_hash(content)
            
            # Check if content has changed
            if chunk_id in self.content_hashes:
                cached_hash = self.content_hashes[chunk_id]
                if cached_hash == current_hash:
                    unchanged_ids.append(chunk_id)
                    continue
            
            # Content is new or changed
            changed_chunks.append(chunk)
        
        logger.info(f"Cache analysis: {len(unchanged_ids)} unchanged, {len(changed_chunks)} changed/new chunks")
        return unchanged_ids, changed_chunks
    
    def update_cache(self, chunks: List[dict], embedding_strategy: str = "unknown"):
        """
        Update cache with newly processed chunks.
        
        Args:
            chunks: List of chunk dictionaries that were just embedded
            embedding_strategy: Strategy used for embedding ("local", "cloud", "hybrid")
        """
        for chunk in chunks:
            chunk_id = chunk['id']
            content = chunk['content']
            content_hash = self._compute_content_hash(content)
            
            # Update content hash
            self.content_hashes[chunk_id] = content_hash
            
            # Update metadata
            self.embedding_metadata[chunk_id] = {
                'strategy': embedding_strategy,
                'timestamp': str(pd.Timestamp.now()) if 'pd' in globals() else str(hash(content_hash)),
                'content_length': len(content),
                'source': chunk.get('metadata', {}).get('source', 'unknown')
            }
        
        # Save to disk
        self._save_cache()
        logger.info(f"Updated cache with {len(chunks)} chunks")
    
    def remove_from_cache(self, chunk_ids: List[str]):
        """
        Remove chunks from cache (e.g., when documents are deleted).
        
        Args:
            chunk_ids: List of chunk IDs to remove
        """
        removed_count = 0
        for chunk_id in chunk_ids:
            if chunk_id in self.content_hashes:
                del self.content_hashes[chunk_id]
                removed_count += 1
            
            if chunk_id in self.embedding_metadata:
                del self.embedding_metadata[chunk_id]
        
        if removed_count > 0:
            self._save_cache()
            logger.info(f"Removed {removed_count} chunks from cache")
    
    def get_cache_stats(self) -> dict:
        """
        Get statistics about the embedding cache.
        
        Returns:
            Dictionary with cache statistics
        """
        strategy_counts = {}
        total_content_length = 0
        
        for metadata in self.embedding_metadata.values():
            strategy = metadata.get('strategy', 'unknown')
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
            total_content_length += metadata.get('content_length', 0)
        
        return {
            'total_chunks': len(self.content_hashes),
            'strategy_distribution': strategy_counts,
            'total_content_length': total_content_length,
            'cache_dir': str(self.cache_dir),
            'cache_files_exist': {
                'hashes': self.hash_cache_file.exists(),
                'metadata': self.metadata_cache_file.exists()
            }
        }
    
    def clear_cache(self):
        """Clear all cache data."""
        self.content_hashes = {}
        self.embedding_metadata = {}
        
        # Remove cache files
        try:
            if self.hash_cache_file.exists():
                self.hash_cache_file.unlink()
            if self.metadata_cache_file.exists():
                self.metadata_cache_file.unlink()
            logger.info("Embedding cache cleared")
        except Exception as e:
            logger.error(f"Failed to clear cache files: {e}")


# Utility function for backward compatibility
def create_embedding_cache(cache_dir: str = "./embedding_cache") -> EmbeddingCache:
    """
    Factory function to create an embedding cache instance.
    
    Args:
        cache_dir: Directory for cache storage
        
    Returns:
        EmbeddingCache instance
    """
    return EmbeddingCache(cache_dir)