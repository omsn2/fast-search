"""
Create Desktop Shortcut for Fast Search Application
This script creates a desktop shortcut with the custom FS icon
"""
import os
import winshell
from win32com.client import Dispatch
from pathlib import Path

def create_desktop_shortcut():
    """Create a desktop shortcut for Fast Search"""
    
    # Get paths
    desktop = winshell.desktop()
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if running from dist (compiled) or source
    if os.path.exists(os.path.join(app_dir, 'dist', 'FastSearch', 'FastSearch.exe')):
        # Compiled version
        target_path = os.path.join(app_dir, 'dist', 'FastSearch', 'FastSearch.exe')
        icon_path = os.path.join(app_dir, 'assets', 'icon.ico')
    else:
        # Source version - create shortcut to batch file
        target_path = os.path.join(app_dir, 'launch-desktop-app.bat')
        icon_path = os.path.join(app_dir, 'assets', 'icon.ico')
    
    # Create shortcut
    shortcut_path = os.path.join(desktop, 'Fast Search.lnk')
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.WorkingDirectory = app_dir
    shortcut.IconLocation = icon_path
    shortcut.Description = 'Fast Search - Lightning-fast desktop file search'
    shortcut.save()
    
    print(f"✓ Desktop shortcut created: {shortcut_path}")
    print(f"  Target: {target_path}")
    print(f"  Icon: {icon_path}")
    return True

if __name__ == '__main__':
    try:
        create_desktop_shortcut()
        print("\n✓ Desktop shortcut created successfully!")
        print("You can now launch Fast Search from your desktop.")
    except Exception as e:
        print(f"✗ Error creating desktop shortcut: {e}")
        print("\nYou can manually create a shortcut by:")
        print("1. Right-click on launch-desktop-app.bat")
        print("2. Select 'Create shortcut'")
        print("3. Move the shortcut to your desktop")
