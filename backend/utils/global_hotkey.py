"""Global keyboard shortcut handler."""
import keyboard
import webbrowser
import threading


class GlobalHotkey:
    """Manage global keyboard shortcuts."""
    
    def __init__(self, hotkey='ctrl+space', on_trigger=None):
        """
        Initialize global hotkey handler.
        
        Args:
            hotkey: Keyboard shortcut (e.g., 'ctrl+space', 'ctrl+shift+f')
            on_trigger: Callback function when hotkey is pressed
        """
        self.hotkey = hotkey
        self.on_trigger = on_trigger or self.default_trigger
        self.registered = False
    
    def default_trigger(self):
        """Default action: open search in browser."""
        print(f"Hotkey {self.hotkey} pressed - opening search...")
        webbrowser.open('http://127.0.0.1:5000')
    
    def register(self):
        """Register the global hotkey."""
        try:
            keyboard.add_hotkey(self.hotkey, self.on_trigger)
            self.registered = True
            print(f"✓ Global hotkey registered: {self.hotkey}")
            return True
        except Exception as e:
            print(f"✗ Failed to register hotkey {self.hotkey}: {e}")
            return False
    
    def unregister(self):
        """Unregister the global hotkey."""
        if self.registered:
            try:
                keyboard.remove_hotkey(self.hotkey)
                self.registered = False
                print(f"✓ Hotkey {self.hotkey} unregistered")
            except Exception as e:
                print(f"✗ Failed to unregister hotkey: {e}")
    
    def wait(self):
        """Keep the hotkey listener running."""
        keyboard.wait()
