"""In-memory cache for search results and file index."""
from functools import lru_cache
from typing import List, Dict, Optional
import time


class SearchCache:
    """LRU cache for search queries and results."""
    
    def __init__(self, cache_size: int = 1000):
        self.cache_size = cache_size
        self.query_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
        self.last_updated = time.time()
    
    def get(self, query: str) -> Optional[List]:
        """Get cached results for a query."""
        normalized_query = query.lower().strip()
        if normalized_query in self.query_cache:
            self.cache_hits += 1
            return self.query_cache[normalized_query]
        self.cache_misses += 1
        return None
    
    def set(self, query: str, results: List):
        """Cache results for a query."""
        normalized_query = query.lower().strip()
        
        # Implement simple LRU by removing oldest if cache is full
        if len(self.query_cache) >= self.cache_size:
            # Remove first (oldest) item
            first_key = next(iter(self.query_cache))
            del self.query_cache[first_key]
        
        self.query_cache[normalized_query] = results
    
    def invalidate(self):
        """Clear all cached results."""
        self.query_cache.clear()
        self.last_updated = time.time()
    
    def get_stats(self) -> Dict:
        """Get cache statistics."""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.query_cache),
            'max_size': self.cache_size,
            'hits': self.cache_hits,
            'misses': self.cache_misses,
            'hit_rate': round(hit_rate, 2),
            'last_updated': self.last_updated
        }


class IndexCache:
    """In-memory cache for the entire file index."""
    
    def __init__(self):
        self.files: List[Dict] = []
        self.last_updated = 0
        self.is_loaded = False
    
    def load(self, files: List[Dict]):
        """Load files into memory."""
        self.files = files
        self.last_updated = time.time()
        self.is_loaded = True
    
    def get_all(self) -> List[Dict]:
        """Get all cached files."""
        return self.files
    
    def add_file(self, file: Dict):
        """Add a single file to cache."""
        # Check if file already exists (by path)
        existing_index = next((i for i, f in enumerate(self.files) if f['path'] == file['path']), None)
        
        if existing_index is not None:
            # Update existing file
            self.files[existing_index] = file
        else:
            # Add new file
            self.files.append(file)
        
        self.last_updated = time.time()
    
    def remove_file(self, path: str):
        """Remove a file from cache by path."""
        self.files = [f for f in self.files if f['path'] != path]
        self.last_updated = time.time()
    
    def update_file(self, path: str, updated_file: Dict):
        """Update a file in cache."""
        for i, f in enumerate(self.files):
            if f['path'] == path:
                self.files[i] = updated_file
                self.last_updated = time.time()
                break
    
    def clear(self):
        """Clear the cache."""
        self.files = []
        self.is_loaded = False
        self.last_updated = 0
    
    def get_stats(self) -> Dict:
        """Get cache statistics."""
        return {
            'file_count': len(self.files),
            'is_loaded': self.is_loaded,
            'last_updated': self.last_updated
        }
