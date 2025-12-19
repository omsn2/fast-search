"""Fuzzy search engine with ranking."""
from typing import List, Dict, Optional
from rapidfuzz import process, fuzz
from backend.config.config import Config
from backend.search.cache import SearchCache


class SearchResult:
    """Search result with score and metadata."""
    
    def __init__(self, name: str, path: str, extension: str, modified_time: int, score: float):
        self.name = name
        self.path = path
        self.extension = extension
        self.modified_time = modified_time
        self.score = score
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'path': self.path,
            'extension': self.extension,
            'modified_time': self.modified_time,
            'score': round(self.score, 2)
        }


class SearchEngine:
    """Fuzzy search engine with intelligent ranking."""
    
    def __init__(self, files: List[Dict], use_cache: bool = True):
        """
        Initialize search engine with file index.
        
        Args:
            files: List of file dictionaries from database
            use_cache: Whether to enable query result caching
        """
        self.files = files
        self.max_results = Config.MAX_RESULTS
        self.fuzzy_threshold = Config.FUZZY_THRESHOLD
        self.use_cache = use_cache
        self.cache = SearchCache(Config.CACHE_SIZE) if use_cache else None
    
    def search(self, query: str) -> List[SearchResult]:
        """
        Search for files matching the query.
        
        Args:
            query: Search query string
            
        Returns:
            List of SearchResult objects, ranked by relevance
        """
        if not query or not self.files:
            return []
        
        query = query.lower().strip()
        
        # Check cache first
        if self.use_cache and self.cache:
            cached_results = self.cache.get(query)
            if cached_results is not None:
                return cached_results
        
        # Extract file names for fuzzy matching
        file_names = [f['name'] for f in self.files]
        
        # Perform fuzzy matching using RapidFuzz
        matches = process.extract(
            query,
            file_names,
            scorer=fuzz.WRatio,  # Weighted ratio for better results
            limit=self.max_results * 2,  # Get more results for re-ranking
            score_cutoff=self.fuzzy_threshold
        )
        
        # Convert to SearchResult objects with enhanced ranking
        results = []
        for match_name, match_score, match_index in matches:
            file = self.files[match_index]
            
            # Calculate final score (70% match score + 30% recency)
            recency_score = self._calculate_recency_score(file['modified_time'])
            final_score = (match_score * 0.7) + (recency_score * 0.3)
            
            results.append(SearchResult(
                name=file['name'],
                path=file['path'],
                extension=file['extension'],
                modified_time=file['modified_time'],
                score=final_score
            ))
        
        # Sort by final score and limit results
        results.sort(key=lambda x: x.score, reverse=True)
        final_results = results[:self.max_results]
        
        # Cache the results
        if self.use_cache and self.cache:
            self.cache.set(query, final_results)
        
        return final_results
    
    def _calculate_recency_score(self, modified_time: int) -> float:
        """
        Calculate recency score (0-100) based on modified time.
        More recent files get higher scores.
        
        Args:
            modified_time: Unix timestamp of file modification
            
        Returns:
            Score from 0 to 100
        """
        import time
        
        current_time = int(time.time())
        age_seconds = current_time - modified_time
        
        # Files modified in last day: 100
        # Files modified in last week: 80
        # Files modified in last month: 60
        # Files modified in last year: 40
        # Older files: 20
        
        if age_seconds < 86400:  # 1 day
            return 100
        elif age_seconds < 604800:  # 1 week
            return 80
        elif age_seconds < 2592000:  # 30 days
            return 60
        elif age_seconds < 31536000:  # 1 year
            return 40
        else:
            return 20
    
    def reload_index(self, files: List[Dict]):
        """Reload the file index (for cache updates)."""
        self.files = files
        # Invalidate cache when index is reloaded
        if self.use_cache and self.cache:
            self.cache.invalidate()
    
    def invalidate_cache(self):
        """Invalidate the query cache."""
        if self.use_cache and self.cache:
            self.cache.invalidate()
    
    def get_cache_stats(self) -> Optional[Dict]:
        """Get cache statistics."""
        if self.use_cache and self.cache:
            return self.cache.get_stats()
        return None

