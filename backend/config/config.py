"""Configuration management for Fast Search."""
import os
from pathlib import Path
from typing import List

class Config:
    """Application configuration."""
    
    # Database
    DB_PATH = Path.home() / ".fast-search" / "index.db"
    
    # Indexing
    DEFAULT_DIRECTORIES: List[str] = [
        str(Path.home() / "Documents"),
        str(Path.home() / "Downloads"),
        str(Path.home() / "Desktop"),
    ]
    
    # System directories to exclude
    EXCLUDED_DIRS = {
        "$Recycle.Bin",
        "Windows.old",
        "$WINDOWS.~BT",
        "System Volume Information",
        "ProgramData",
        "AppData",
        "node_modules",
        ".git",
        "__pycache__",
        "venv",
        "env",
    }
    
    # Search
    MAX_RESULTS = 50
    FUZZY_THRESHOLD = 60  # Minimum match score (0-100)
    
    # Performance
    BATCH_SIZE = 1000  # Files to insert at once
    CACHE_SIZE = 1000  # Number of queries to cache
    
    @classmethod
    def ensure_db_directory(cls):
        """Create database directory if it doesn't exist."""
        cls.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
