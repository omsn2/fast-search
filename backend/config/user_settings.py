"""User settings manager for indexed directories."""
import json
import os
from pathlib import Path
from typing import List


class UserSettings:
    """Manage user settings for indexed directories."""
    
    def __init__(self, settings_file: str = None):
        if settings_file is None:
            settings_file = str(Path.home() / ".fast-search" / "settings.json")
        
        self.settings_file = settings_file
        self.settings = self._load_settings()
    
    def _load_settings(self) -> dict:
        """Load settings from file."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default settings
        return {
            'indexed_directories': []
        }
    
    def _save_settings(self):
        """Save settings to file."""
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get_indexed_directories(self) -> List[str]:
        """Get list of indexed directories."""
        return self.settings.get('indexed_directories', [])
    
    def add_directory(self, directory: str) -> bool:
        """Add a directory to index."""
        directory = os.path.abspath(directory)
        
        if not os.path.exists(directory):
            return False
        
        if not os.path.isdir(directory):
            return False
        
        directories = self.get_indexed_directories()
        if directory not in directories:
            directories.append(directory)
            self.settings['indexed_directories'] = directories
            self._save_settings()
        
        return True
    
    def remove_directory(self, directory: str) -> bool:
        """Remove a directory from index."""
        directory = os.path.abspath(directory)
        directories = self.get_indexed_directories()
        
        if directory in directories:
            directories.remove(directory)
            self.settings['indexed_directories'] = directories
            self._save_settings()
            return True
        
        return False
    
    def clear_directories(self):
        """Clear all indexed directories."""
        self.settings['indexed_directories'] = []
        self._save_settings()
