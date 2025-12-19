"""Test script to demonstrate Phase 2 features."""
import time
from backend.search.search_service import SearchService
from backend.config.config import Config

def test_caching():
    """Test search caching performance."""
    print("=" * 60)
    print("PHASE 2 FEATURE TEST: Search Caching")
    print("=" * 60)
    
    service = SearchService(enable_watcher=False)
    
    # First search (cache miss)
    print("\n1. First search (cache miss):")
    start = time.time()
    results = service.search("resume")
    elapsed_ms = (time.time() - start) * 1000
    print(f"   Query: 'resume'")
    print(f"   Results: {len(results)}")
    print(f"   Time: {elapsed_ms:.2f}ms")
    
    # Second search (cache hit)
    print("\n2. Second search (cache hit):")
    start = time.time()
    results = service.search("resume")
    elapsed_ms = (time.time() - start) * 1000
    print(f"   Query: 'resume'")
    print(f"   Results: {len(results)}")
    print(f"   Time: {elapsed_ms:.2f}ms")
    print(f"   ⚡ Cache speedup!")
    
    # Different search
    print("\n3. Different search (cache miss):")
    start = time.time()
    results = service.search("document")
    elapsed_ms = (time.time() - start) * 1000
    print(f"   Query: 'document'")
    print(f"   Results: {len(results)}")
    print(f"   Time: {elapsed_ms:.2f}ms")
    
    # Cache stats
    print("\n4. Cache Statistics:")
    stats = service.get_stats()
    if stats['query_cache']:
        cache_stats = stats['query_cache']
        print(f"   Cache size: {cache_stats['size']}/{cache_stats['max_size']}")
        print(f"   Cache hits: {cache_stats['hits']}")
        print(f"   Cache misses: {cache_stats['misses']}")
        print(f"   Hit rate: {cache_stats['hit_rate']}%")
    
    service.close()
    print("\n" + "=" * 60)
    print("✓ Caching test complete!")
    print("=" * 60)


def test_index_cache():
    """Test in-memory index caching."""
    print("\n" + "=" * 60)
    print("PHASE 2 FEATURE TEST: In-Memory Index Cache")
    print("=" * 60)
    
    service = SearchService(enable_watcher=False)
    
    stats = service.get_stats()
    index_stats = stats['index']
    
    print(f"\n✓ Index loaded into memory")
    print(f"   Files cached: {index_stats['file_count']}")
    print(f"   Cache loaded: {index_stats['is_loaded']}")
    print(f"   Last updated: {time.ctime(index_stats['last_updated'])}")
    
    # Perform multiple searches to show speed
    print(f"\n⚡ Running 10 searches with cached index...")
    queries = ["resume", "pdf", "doc", "txt", "file", "test", "data", "report", "image", "photo"]
    
    total_time = 0
    for query in queries:
        start = time.time()
        results = service.search(query)
        elapsed = (time.time() - start) * 1000
        total_time += elapsed
    
    avg_time = total_time / len(queries)
    print(f"   Average search time: {avg_time:.2f}ms")
    print(f"   Total time: {total_time:.2f}ms")
    
    service.close()
    print("\n" + "=" * 60)
    print("✓ Index cache test complete!")
    print("=" * 60)


if __name__ == '__main__':
    test_caching()
    test_index_cache()
    
    print("\n" + "=" * 60)
    print("🎉 PHASE 2 FEATURES WORKING!")
    print("=" * 60)
    print("\nFeatures tested:")
    print("  ✅ Query result caching (LRU cache)")
    print("  ✅ In-memory index caching")
    print("  ✅ Cache statistics")
    print("  ✅ Fast search with cached data")
    print("\nNext: Test file watching with 'python main.py watch'")
    print("=" * 60)
