"""
Hotkey validation and parsing utilities for Fast Search
"""

# Reserved system hotkeys that should never be allowed
RESERVED_HOTKEYS = [
    "ctrl+alt+delete",
    "ctrl+alt+del",
    "win+l",
    "alt+tab",
    "alt+f4",
    "ctrl+shift+esc",
    "win+d",
    "win+e",
    "win+r",
]

# Common application hotkeys (warn but allow)
COMMON_CONFLICTS = [
    "ctrl+c",
    "ctrl+v",
    "ctrl+x",
    "ctrl+z",
    "ctrl+y",
    "ctrl+s",
    "ctrl+a",
    "ctrl+f",
    "ctrl+p",
]

VALID_MODIFIERS = ["ctrl", "shift", "alt", "win"]

VALID_KEYS = [
    # Letters
    *[chr(i) for i in range(ord('a'), ord('z') + 1)],
    # Numbers
    *[str(i) for i in range(10)],
    # Function keys
    *[f"f{i}" for i in range(1, 13)],
    # Special keys
    "space", "enter", "tab", "backspace", "delete",
    "home", "end", "pageup", "pagedown",
    "up", "down", "left", "right",
    "insert", "escape", "esc"
]


def parse_hotkey_string(hotkey_str):
    """
    Parse a hotkey string like 'ctrl+shift+f' into components
    
    Args:
        hotkey_str: String representation of hotkey (e.g., "ctrl+shift+f")
        
    Returns:
        tuple: (modifiers_list, key, is_valid)
    """
    if not hotkey_str:
        return [], None, False
    
    parts = [p.strip().lower() for p in hotkey_str.split('+')]
    
    if len(parts) < 2:
        return [], None, False
    
    modifiers = parts[:-1]
    key = parts[-1]
    
    # Validate modifiers
    for mod in modifiers:
        if mod not in VALID_MODIFIERS:
            return [], None, False
    
    # Validate key
    if key not in VALID_KEYS:
        return [], None, False
    
    return modifiers, key, True


def validate_hotkey(hotkey_str):
    """
    Validate a hotkey combination
    
    Args:
        hotkey_str: String representation of hotkey
        
    Returns:
        tuple: (is_valid, error_message, warning_message)
    """
    modifiers, key, is_valid = parse_hotkey_string(hotkey_str)
    
    if not is_valid:
        return False, "Invalid hotkey format. Use format like 'ctrl+shift+f'", None
    
    # Must have at least one modifier
    if not modifiers:
        return False, "Hotkey must include at least one modifier (Ctrl, Shift, Alt, Win)", None
    
    # Check if reserved
    if hotkey_str.lower() in RESERVED_HOTKEYS:
        return False, f"'{hotkey_str}' is a reserved system hotkey and cannot be used", None
    
    # Check for common conflicts (warning only)
    warning = None
    if hotkey_str.lower() in COMMON_CONFLICTS:
        warning = f"'{hotkey_str}' is commonly used by other applications. This may cause conflicts."
    
    return True, None, warning


def format_hotkey_display(modifiers, key):
    """
    Format hotkey for display (capitalize properly)
    
    Args:
        modifiers: List of modifier keys
        key: Main key
        
    Returns:
        str: Formatted hotkey string (e.g., "Ctrl+Shift+F")
    """
    display_mods = []
    for mod in modifiers:
        if mod == "ctrl":
            display_mods.append("Ctrl")
        elif mod == "shift":
            display_mods.append("Shift")
        elif mod == "alt":
            display_mods.append("Alt")
        elif mod == "win":
            display_mods.append("Win")
    
    display_key = key.capitalize() if len(key) == 1 else key.title()
    
    return "+".join(display_mods + [display_key])
