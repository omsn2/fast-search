"""File system indexer."""
import os
from pathlib import Path
from typing import List, Generator
from backend.database.database import FileMetadata
from backend.config.config import Config


class FileIndexer:
    """Recursively scan and index files."""
    
    def __init__(self):
        self.excluded_dirs = Config.EXCLUDED_DIRS
    
    def _should_skip_directory(self, dir_name: str) -> bool:
        """Check if directory should be skipped."""
        return dir_name in self.excluded_dirs or dir_name.startswith('.')
    
    def scan_directory(self, root_path: str) -> Generator[FileMetadata, None, None]:
        """
        Recursively scan directory and yield file metadata.
        
        Args:
            root_path: Root directory to scan
            
        Yields:
            FileMetadata objects for each file found
        """
        root_path = Path(root_path)
        
        if not root_path.exists():
            print(f"Warning: Path does not exist: {root_path}")
            return
        
        if not root_path.is_dir():
            print(f"Warning: Path is not a directory: {root_path}")
            return
        
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Filter out excluded directories (modifies in-place)
            dirnames[:] = [d for d in dirnames if not self._should_skip_directory(d)]
            
            for filename in filenames:
                try:
                    file_path = Path(dirpath) / filename
                    
                    # Skip if file doesn't exist (race condition)
                    if not file_path.exists():
                        continue
                    
                    # Get file metadata
                    stat = file_path.stat()
                    extension = file_path.suffix.lower() if file_path.suffix else ''
                    
                    yield FileMetadata(
                        name=filename,
                        path=str(file_path),
                        extension=extension,
                        modified_time=int(stat.st_mtime)
                    )
                    
                except (PermissionError, OSError) as e:
                    # Skip files we can't access
                    print(f"Skipping {filename}: {e}")
                    continue
    
    def index_directories(self, directories: List[str], batch_size: int = Config.BATCH_SIZE) -> Generator[List[FileMetadata], None, None]:
        """
        Index multiple directories in batches.
        
        Args:
            directories: List of directory paths to index
            batch_size: Number of files per batch
            
        Yields:
            Batches of FileMetadata objects
        """
        batch = []
        
        for directory in directories:
            print(f"Indexing: {directory}")
            
            for file_metadata in self.scan_directory(directory):
                batch.append(file_metadata)
                
                if len(batch) >= batch_size:
                    yield batch
                    batch = []
        
        # Yield remaining files
        if batch:
            yield batch
