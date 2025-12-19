"""Auto-start on Windows boot functionality."""
import os
import sys
import winreg
from pathlib import Path


class AutoStart:
    """Manage Windows startup registry entry."""
    
    APP_NAME = "FastSearch"
    
    @staticmethod
    def get_executable_path():
        """Get the path to the executable or script."""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            return sys.executable
        else:
            # Running as script - create a batch file launcher
            script_dir = Path(__file__).parent.parent.parent
            launcher_path = script_dir / "fast-search-startup.bat"
            
            # Create startup batch file
            python_exe = sys.executable
            main_script = script_dir / "desktop_app.py"
            
            with open(launcher_path, 'w') as f:
                f.write(f'@echo off\n')
                f.write(f'start "" "{python_exe}" "{main_script}"\n')
            
            return str(launcher_path)
    
    @staticmethod
    def is_enabled():
        """Check if auto-start is enabled."""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            
            try:
                winreg.QueryValueEx(key, AutoStart.APP_NAME)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception as e:
            print(f"Error checking auto-start: {e}")
            return False
    
    @staticmethod
    def enable():
        """Enable auto-start on Windows boot."""
        try:
            exe_path = AutoStart.get_executable_path()
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            winreg.SetValueEx(
                key,
                AutoStart.APP_NAME,
                0,
                winreg.REG_SZ,
                exe_path
            )
            
            winreg.CloseKey(key)
            print(f"✓ Auto-start enabled: {exe_path}")
            return True
        except Exception as e:
            print(f"✗ Failed to enable auto-start: {e}")
            return False
    
    @staticmethod
    def disable():
        """Disable auto-start on Windows boot."""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            try:
                winreg.DeleteValue(key, AutoStart.APP_NAME)
                winreg.CloseKey(key)
                print("✓ Auto-start disabled")
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return True  # Already disabled
        except Exception as e:
            print(f"✗ Failed to disable auto-start: {e}")
            return False
    
    @staticmethod
    def toggle():
        """Toggle auto-start on/off."""
        if AutoStart.is_enabled():
            return AutoStart.disable()
        else:
            return AutoStart.enable()
