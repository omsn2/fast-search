"""File system watcher for incremental index updates."""
import time
from pathlib import Path
from typing import Callable, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from backend.database.database import FileMetadata


class IndexUpdateHandler(FileSystemEventHandler):
    """Handle file system events and update index."""
    
    def __init__(self, 
                 on_created: Callable[[str], None],
                 on_modified: Callable[[str], None],
                 on_deleted: Callable[[str], None],
                 on_moved: Callable[[str, str], None],
                 excluded_dirs: Set[str]):
        self.on_created_callback = on_created
        self.on_modified_callback = on_modified
        self.on_deleted_callback = on_deleted
        self.on_moved_callback = on_moved
        self.excluded_dirs = excluded_dirs
        
        # Debouncing: track recent events to avoid duplicates
        self.recent_events = {}
        self.debounce_seconds = 0.5
    
    def _should_skip(self, path: str) -> bool:
        """Check if path should be skipped."""
        path_obj = Path(path)
        
        # Skip directories
        if path_obj.is_dir():
            return True
        
        # Skip excluded directories
        for part in path_obj.parts:
            if part in self.excluded_dirs or part.startswith('.'):
                return True
        
        return False
    
    def _is_duplicate_event(self, event_key: str) -> bool:
        """Check if this is a duplicate event (debouncing)."""
        current_time = time.time()
        
        if event_key in self.recent_events:
            last_time = self.recent_events[event_key]
            if current_time - last_time < self.debounce_seconds:
                return True
        
        self.recent_events[event_key] = current_time
        
        # Clean up old events
        self.recent_events = {
            k: v for k, v in self.recent_events.items() 
            if current_time - v < self.debounce_seconds * 2
        }
        
        return False
    
    def on_created(self, event: FileSystemEvent):
        """Handle file creation."""
        if self._should_skip(event.src_path):
            return
        
        event_key = f"created:{event.src_path}"
        if self._is_duplicate_event(event_key):
            return
        
        print(f"[Watcher] File created: {event.src_path}")
        self.on_created_callback(event.src_path)
    
    def on_modified(self, event: FileSystemEvent):
        """Handle file modification."""
        if self._should_skip(event.src_path):
            return
        
        event_key = f"modified:{event.src_path}"
        if self._is_duplicate_event(event_key):
            return
        
        print(f"[Watcher] File modified: {event.src_path}")
        self.on_modified_callback(event.src_path)
    
    def on_deleted(self, event: FileSystemEvent):
        """Handle file deletion."""
        if self._should_skip(event.src_path):
            return
        
        event_key = f"deleted:{event.src_path}"
        if self._is_duplicate_event(event_key):
            return
        
        print(f"[Watcher] File deleted: {event.src_path}")
        self.on_deleted_callback(event.src_path)
    
    def on_moved(self, event: FileSystemEvent):
        """Handle file move/rename."""
        if hasattr(event, 'dest_path'):
            if self._should_skip(event.src_path) and self._should_skip(event.dest_path):
                return
            
            event_key = f"moved:{event.src_path}:{event.dest_path}"
            if self._is_duplicate_event(event_key):
                return
            
            print(f"[Watcher] File moved: {event.src_path} -> {event.dest_path}")
            self.on_moved_callback(event.src_path, event.dest_path)


class FileWatcher:
    """Monitor file system changes and update index incrementally."""
    
    def __init__(self,
                 on_created: Callable[[str], None],
                 on_modified: Callable[[str], None],
                 on_deleted: Callable[[str], None],
                 on_moved: Callable[[str, str], None],
                 excluded_dirs: Set[str]):
        self.observer = Observer()
        self.event_handler = IndexUpdateHandler(
            on_created, on_modified, on_deleted, on_moved, excluded_dirs
        )
        self.watched_paths = []
    
    def add_directory(self, directory: str):
        """Add a directory to watch."""
        path = Path(directory)
        if not path.exists() or not path.is_dir():
            print(f"Warning: Cannot watch {directory} - not a valid directory")
            return
        
        self.observer.schedule(self.event_handler, str(path), recursive=True)
        self.watched_paths.append(str(path))
        print(f"[Watcher] Now watching: {directory}")
    
    def start(self):
        """Start watching for file system changes."""
        if not self.watched_paths:
            print("[Watcher] No directories to watch")
            return
        
        self.observer.start()
        print(f"[Watcher] Started monitoring {len(self.watched_paths)} directories")
    
    def stop(self):
        """Stop watching."""
        self.observer.stop()
        self.observer.join()
        print("[Watcher] Stopped monitoring")
    
    def is_alive(self) -> bool:
        """Check if watcher is running."""
        return self.observer.is_alive()
