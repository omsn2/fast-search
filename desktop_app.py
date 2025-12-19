"""Enhanced desktop application with system tray and global hotkey."""
import webview
import threading
import time
import sys
import os
import webbrowser

# Add desktop-ui to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'desktop-ui'))
sys.path.insert(0, os.path.dirname(__file__))

from app import run_server
from backend.utils.system_tray import SystemTray
from backend.utils.global_hotkey import GlobalHotkey


class FastSearchApp:
    """Main application with system tray and global hotkey."""
    
    def __init__(self):
        self.flask_thread = None
        self.tray = None
        self.hotkey = None
        self.window = None
        self.server_running = False
    
    def start_flask(self):
        """Start Flask server in a separate thread."""
        print("[App] Starting Flask server...")
        self.server_running = True
        run_server(port=5000, debug=False)
    
    def show_window(self):
        """Show or focus the search window."""
        print("[App] Opening search window...")
        webbrowser.open('http://127.0.0.1:5000')
    
    def show_settings(self):
        """Show the settings page."""
        print("[App] Opening settings...")
        webbrowser.open('http://127.0.0.1:5000/settings')
    
    def quit_app(self):
        """Quit the application."""
        print("[App] Shutting down...")
        if self.hotkey:
            self.hotkey.unregister()
        sys.exit(0)
    
    def run(self, use_tray=True, use_hotkey=True):
        """Run the application."""
        print("=" * 60)
        print("Fast Search - Desktop Application")
        print("=" * 60)
        
        # Start Flask server
        self.flask_thread = threading.Thread(target=self.start_flask, daemon=True)
        self.flask_thread.start()
        
        # Wait for server to start
        print("[App] Waiting for server to start...")
        time.sleep(2)
        
        # Set up system tray
        if use_tray:
            print("[App] Setting up system tray...")
            self.tray = SystemTray(
                on_show=self.show_window,
                on_settings=self.show_settings,
                on_quit=self.quit_app
            )
            tray_thread = self.tray.start_in_thread()
        
        # Set up global hotkey
        if use_hotkey:
            print("[App] Setting up global hotkey (Ctrl+Space)...")
            self.hotkey = GlobalHotkey(
                hotkey='ctrl+space',
                on_trigger=self.show_window
            )
            
            # Try to register hotkey (may fail if not admin)
            if not self.hotkey.register():
                print("[App] ⚠ Could not register global hotkey")
                print("[App] ⚠ Try running as administrator for hotkey support")
        
        # Open browser window
        print("[App] Opening browser...")
        time.sleep(1)
        self.show_window()
        
        print("\n" + "=" * 60)
        print("✓ Fast Search is running!")
        print("=" * 60)
        print("\nFeatures:")
        if use_tray:
            print("  • System Tray: Right-click the tray icon for options")
        if use_hotkey and self.hotkey and self.hotkey.registered:
            print("  • Global Hotkey: Press Ctrl+Space to open search")
        print("  • Web Interface: http://127.0.0.1:5000")
        print("\nPress Ctrl+C to quit")
        print("=" * 60 + "\n")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[App] Received interrupt signal")
            self.quit_app()


def main():
    """Main entry point."""
    app = FastSearchApp()
    app.run(use_tray=True, use_hotkey=True)


if __name__ == '__main__':
    main()
