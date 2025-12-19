"""Search service with integrated caching and file watching."""
from pathlib import Path
from typing import List, Optional
import time
from backend.database.database import Database, FileMetadata
from backend.search.search_engine import SearchEngine
from backend.search.cache import IndexCache
from backend.indexer.file_watcher import FileWatcher
from backend.config.config import Config


class SearchService:
    """Unified search service with caching and file watching."""
    
    def __init__(self, enable_watcher: bool = False):
        """
        Initialize search service.
        
        Args:
            enable_watcher: Whether to enable file system watching
        """
        self.db = Database()
        self.index_cache = IndexCache()
        self.search_engine: Optional[SearchEngine] = None
        self.file_watcher: Optional[FileWatcher] = None
        self.enable_watcher = enable_watcher
        self.watched_directories: List[str] = []
        
        # Load index into memory
        self._load_index()
    
    def _load_index(self):
        """Load file index from database into memory."""
        print("[Service] Loading index from database...")
        files = self.db.get_all_files()
        self.index_cache.load(files)
        self.search_engine = SearchEngine(files, use_cache=True)
        print(f"[Service] Loaded {len(files)} files into memory")
    
    def _on_file_created(self, path: str):
        """Handle file creation event."""
        try:
            file_path = Path(path)
            if not file_path.exists():
                return
            
            stat = file_path.stat()
            metadata = FileMetadata(
                name=file_path.name,
                path=str(file_path),
                extension=file_path.suffix.lower() if file_path.suffix else '',
                modified_time=int(stat.st_mtime)
            )
            
            # Update database
            self.db.insert_files([metadata])
            
            # Update cache
            self.index_cache.add_file(metadata.to_dict())
            
            # Reload search engine and invalidate query cache
            if self.search_engine:
                self.search_engine.reload_index(self.index_cache.get_all())
            
            print(f"[Service] Added: {file_path.name}")
        except Exception as e:
            print(f"[Service] Error adding file {path}: {e}")
    
    def _on_file_modified(self, path: str):
        """Handle file modification event."""
        try:
            file_path = Path(path)
            if not file_path.exists():
                return
            
            stat = file_path.stat()
            metadata = FileMetadata(
                name=file_path.name,
                path=str(file_path),
                extension=file_path.suffix.lower() if file_path.suffix else '',
                modified_time=int(stat.st_mtime)
            )
            
            # Update database
            self.db.update_file(str(file_path), metadata)
            
            # Update cache
            self.index_cache.update_file(str(file_path), metadata.to_dict())
            
            # Reload search engine
            if self.search_engine:
                self.search_engine.reload_index(self.index_cache.get_all())
            
            print(f"[Service] Updated: {file_path.name}")
        except Exception as e:
            print(f"[Service] Error updating file {path}: {e}")
    
    def _on_file_deleted(self, path: str):
        """Handle file deletion event."""
        try:
            # Update database
            self.db.delete_file(path)
            
            # Update cache
            self.index_cache.remove_file(path)
            
            # Reload search engine
            if self.search_engine:
                self.search_engine.reload_index(self.index_cache.get_all())
            
            print(f"[Service] Deleted: {Path(path).name}")
        except Exception as e:
            print(f"[Service] Error deleting file {path}: {e}")
    
    def _on_file_moved(self, src_path: str, dest_path: str):
        """Handle file move/rename event."""
        try:
            # Delete old path
            self.db.delete_file(src_path)
            self.index_cache.remove_file(src_path)
            
            # Add new path
            dest_file = Path(dest_path)
            if dest_file.exists():
                stat = dest_file.stat()
                metadata = FileMetadata(
                    name=dest_file.name,
                    path=str(dest_file),
                    extension=dest_file.suffix.lower() if dest_file.suffix else '',
                    modified_time=int(stat.st_mtime)
                )
                self.db.insert_files([metadata])
                self.index_cache.add_file(metadata.to_dict())
            
            # Reload search engine
            if self.search_engine:
                self.search_engine.reload_index(self.index_cache.get_all())
            
            print(f"[Service] Moved: {Path(src_path).name} -> {dest_file.name}")
        except Exception as e:
            print(f"[Service] Error moving file {src_path} -> {dest_path}: {e}")
    
    def start_watching(self, directories: List[str]):
        """Start watching directories for changes."""
        if not self.enable_watcher:
            print("[Service] File watching is disabled")
            return
        
        if self.file_watcher and self.file_watcher.is_alive():
            print("[Service] File watcher already running")
            return
        
        self.watched_directories = directories
        self.file_watcher = FileWatcher(
            on_created=self._on_file_created,
            on_modified=self._on_file_modified,
            on_deleted=self._on_file_deleted,
            on_moved=self._on_file_moved,
            excluded_dirs=Config.EXCLUDED_DIRS
        )
        
        for directory in directories:
            self.file_watcher.add_directory(directory)
        
        self.file_watcher.start()
    
    def stop_watching(self):
        """Stop watching for file changes."""
        if self.file_watcher and self.file_watcher.is_alive():
            self.file_watcher.stop()
            print("[Service] Stopped file watching")
    
    def search(self, query: str):
        """Search for files."""
        if not self.search_engine:
            return []
        return self.search_engine.search(query)
    
    def get_stats(self):
        """Get service statistics."""
        cache_stats = self.search_engine.get_cache_stats() if self.search_engine else None
        index_stats = self.index_cache.get_stats()
        
        return {
            'index': index_stats,
            'query_cache': cache_stats,
            'watching': self.file_watcher.is_alive() if self.file_watcher else False,
            'watched_directories': self.watched_directories
        }
    
    def close(self):
        """Clean up resources."""
        self.stop_watching()
        self.db.close()
