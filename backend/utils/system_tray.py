"""System tray integration for Fast Search."""
import pystray
from PIL import Image, ImageDraw
import threading
import webbrowser
import sys
import os


class SystemTray:
    """System tray icon and menu."""
    
    def __init__(self, on_show=None, on_settings=None, on_quit=None):
        self.on_show = on_show
        self.on_settings = on_settings
        self.on_quit = on_quit
        self.icon = None
        self.running = False
    
    def create_icon_image(self):
        """Create a simple icon image."""
        # Create a 64x64 image with a search icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='#6366f1')
        dc = ImageDraw.Draw(image)
        
        # Draw a simple magnifying glass
        # Circle
        dc.ellipse([16, 16, 40, 40], outline='white', width=3)
        # Handle
        dc.line([36, 36, 48, 48], fill='white', width=3)
        
        return image
    
    def show_window(self, icon=None, item=None):
        """Show the main search window."""
        if self.on_show:
            self.on_show()
        else:
            webbrowser.open('http://127.0.0.1:5000')
    
    def show_settings(self, icon=None, item=None):
        """Show the settings page."""
        if self.on_settings:
            self.on_settings()
        else:
            webbrowser.open('http://127.0.0.1:5000/settings')
    
    def quit_app(self, icon=None, item=None):
        """Quit the application."""
        print("Quitting Fast Search...")
        self.running = False
        if self.icon:
            self.icon.stop()
        if self.on_quit:
            self.on_quit()
        sys.exit(0)
    
    def create_menu(self):
        """Create the system tray menu."""
        return pystray.Menu(
            pystray.MenuItem('Show Search', self.show_window, default=True),
            pystray.MenuItem('Settings', self.show_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Quit', self.quit_app)
        )
    
    def run(self):
        """Run the system tray icon."""
        self.running = True
        image = self.create_icon_image()
        menu = self.create_menu()
        
        self.icon = pystray.Icon(
            'fast_search',
            image,
            'Fast Search',
            menu
        )
        
        print("System tray icon started")
        self.icon.run()
    
    def start_in_thread(self):
        """Start the system tray in a background thread."""
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        return thread
