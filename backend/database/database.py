"""Database operations for file indexing."""
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from backend.config.config import Config


class FileMetadata:
    """File metadata structure."""
    
    def __init__(self, name: str, path: str, extension: str, modified_time: int):
        self.name = name
        self.path = path
        self.extension = extension
        self.modified_time = modified_time
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'path': self.path,
            'extension': self.extension,
            'modified_time': self.modified_time
        }


class Database:
    """SQLite database manager for file index."""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Config.DB_PATH
        Config.ensure_db_directory()
        self.conn = None
        self._initialize_db()
    
    def _initialize_db(self):
        """Create database and tables if they don't exist."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT UNIQUE NOT NULL,
                extension TEXT,
                modified_time INTEGER,
                created_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
        """)
        
        # Create indexes for faster queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON files(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_path ON files(path)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_modified ON files(modified_time DESC)")
        
        self.conn.commit()
    
    def insert_files(self, files: List[FileMetadata]) -> int:
        """Batch insert files into database."""
        cursor = self.conn.cursor()
        inserted = 0
        
        for file in files:
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO files (name, path, extension, modified_time)
                    VALUES (?, ?, ?, ?)
                """, (file.name, file.path, file.extension, file.modified_time))
                inserted += 1
            except sqlite3.Error as e:
                print(f"Error inserting {file.path}: {e}")
        
        self.conn.commit()
        return inserted
    
    def update_file(self, path: str, metadata: FileMetadata) -> bool:
        """Update a single file's metadata."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE files 
                SET name = ?, extension = ?, modified_time = ?
                WHERE path = ?
            """, (metadata.name, metadata.extension, metadata.modified_time, path))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating {path}: {e}")
            return False
    
    def delete_file(self, path: str) -> bool:
        """Remove a file from the index."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM files WHERE path = ?", (path,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting {path}: {e}")
            return False
    
    def get_all_files(self) -> List[Dict]:
        """Retrieve all indexed files."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, path, extension, modified_time FROM files")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_file_count(self) -> int:
        """Get total number of indexed files."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM files")
        return cursor.fetchone()[0]
    
    def clear_index(self):
        """Clear all files from the index."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM files")
        self.conn.commit()
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
