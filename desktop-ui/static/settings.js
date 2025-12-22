// Settings Page JavaScript

let indexedDirectories = [];

// Load settings on page load
async function loadSettings() {
    try {
        // Load indexed directories
        const response = await fetch('/api/settings/directories');
        const data = await response.json();
        
        indexedDirectories = data.directories || [];
        displayDirectories();
        
        // Load excluded directories
        const excludedResponse = await fetch('/api/settings/excluded');
        const excludedData = await excludedResponse.json();
        displayExcluded(excludedData.excluded || []);
        
    } catch (error) {
        showStatus('Failed to load settings', 'error');
    }
}

// Display directories
function displayDirectories() {
    const listEl = document.getElementById('directoryList');
    
    if (indexedDirectories.length === 0) {
        listEl.innerHTML = `
            <div style="text-align: center; padding: 20px; color: var(--text-muted);">
                No directories indexed yet. Add one to get started!
            </div>
        `;
        return;
    }
    
    listEl.innerHTML = indexedDirectories.map((dir, index) => `
        <div class="directory-item">
            <div class="directory-path">${escapeHtml(dir)}</div>
            <button class="btn btn-danger" data-dir-index="${index}">Remove</button>
        </div>
    `).join('');
    
    // Attach event listeners to remove buttons
    const removeButtons = listEl.querySelectorAll('.btn-danger');
    removeButtons.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            removeDirectory(indexedDirectories[index]);
        });
    });
}

// Display excluded directories
function displayExcluded(excluded) {
    const el = document.getElementById('excludedDirs');
    el.innerHTML = excluded.map(dir => `• ${dir}`).join('<br>');
}

// Add directory
async function addDirectory() {
    const input = document.getElementById('newDirectory');
    const directory = input.value.trim();
    
    if (!directory) {
        showStatus('Please enter a directory path', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/settings/directories/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ directory })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`Added and indexing: ${directory}`, 'success');
            input.value = '';
            loadSettings();
        } else {
            showStatus(data.error || 'Failed to add directory', 'error');
        }
    } catch (error) {
        showStatus('Failed to add directory', 'error');
    }
}

// Remove directory
async function removeDirectory(directory) {
    if (!confirm(`Remove "${directory}" from index?`)) {
        return;
    }
    
    try {
        const response = await fetch('/api/settings/directories/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ directory })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`Removed: ${directory}`, 'success');
            loadSettings();
        } else {
            showStatus(data.error || 'Failed to remove directory', 'error');
        }
    } catch (error) {
        showStatus('Failed to remove directory', 'error');
    }
}

// Reindex all
async function reindexAll() {
    if (!confirm('Reindex all directories? This may take a few minutes.')) {
        return;
    }
    
    showStatus('Reindexing... This may take a while.', 'success');
    
    try {
        const response = await fetch('/api/settings/reindex', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`Reindexed ${data.count} files successfully!`, 'success');
        } else {
            showStatus(data.error || 'Failed to reindex', 'error');
        }
    } catch (error) {
        showStatus('Failed to reindex', 'error');
    }
}

// Show status message
function showStatus(message, type) {
    const statusEl = document.getElementById('statusMessage');
    statusEl.className = `status-message status-${type}`;
    statusEl.textContent = message;
    statusEl.style.display = 'block';
    
    setTimeout(() => {
        statusEl.style.display = 'none';
    }, 5000);
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Toggle auto-start
async function toggleAutoStart() {
    const checkbox = document.getElementById('autostartToggle');
    
    try {
        const response = await fetch('/api/settings/autostart/toggle', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            checkbox.checked = data.enabled;
            showStatus(
                data.enabled ? 'Auto-start enabled' : 'Auto-start disabled',
                'success'
            );
        } else {
            // Revert checkbox
            checkbox.checked = !checkbox.checked;
            showStatus(data.error || 'Failed to toggle auto-start', 'error');
        }
    } catch (error) {
        // Revert checkbox
        checkbox.checked = !checkbox.checked;
        showStatus('Failed to toggle auto-start', 'error');
    }
}

// Load auto-start status
async function loadAutoStartStatus() {
    try {
        const response = await fetch('/api/settings/autostart/status');
        const data = await response.json();
        
        const checkbox = document.getElementById('autostartToggle');
        if (checkbox) {
            checkbox.checked = data.enabled || false;
        }
    } catch (error) {
        console.error('Failed to load auto-start status:', error);
    }
}

// ===== Hotkey Settings =====

let capturingHotkey = false;
let currentHotkey = '';
let pressedKeys = new Set();

// Load current hotkey
async function loadCurrentHotkey() {
    try {
        const response = await fetch('/api/settings/hotkey');
        const data = await response.json();
        currentHotkey = data.combination || 'ctrl+space';
        document.getElementById('hotkeyInput').value = formatHotkeyDisplay(currentHotkey);
    } catch (error) {
        console.error('Failed to load hotkey:', error);
        document.getElementById('hotkeyInput').value = 'Ctrl+Space';
    }
}

// Format hotkey for display
function formatHotkeyDisplay(hotkey) {
    return hotkey.split('+').map(part => {
        if (part === 'ctrl') return 'Ctrl';
        if (part === 'shift') return 'Shift';
        if (part === 'alt') return 'Alt';
        if (part === 'win') return 'Win';
        return part.charAt(0).toUpperCase() + part.slice(1);
    }).join('+');
}

// Hotkey input focus
const hotkeyInput = document.getElementById('hotkeyInput');
hotkeyInput.addEventListener('focus', () => {
    capturingHotkey = true;
    pressedKeys.clear();
    hotkeyInput.style.borderColor = 'var(--primary)';
    hotkeyInput.style.boxShadow = '0 0 0 3px rgba(99, 102, 241, 0.2)';
    document.getElementById('hotkeyStatus').textContent = 'Press your key combination...';
    document.getElementById('hotkeyStatus').style.color = 'var(--primary)';
});

// Hotkey input blur
hotkeyInput.addEventListener('blur', () => {
    setTimeout(() => {
        capturingHotkey = false;
        pressedKeys.clear();
        hotkeyInput.style.borderColor = 'var(--border)';
        hotkeyInput.style.boxShadow = 'none';
        document.getElementById('hotkeyStatus').textContent = '';
    }, 200);
});

// Capture hotkey
hotkeyInput.addEventListener('keydown', async (e) => {
    if (!capturingHotkey) return;
    
    e.preventDefault();
    
    // Add key to pressed keys
    const key = e.key.toLowerCase();
    
    // Track modifiers
    if (e.ctrlKey) pressedKeys.add('ctrl');
    if (e.shiftKey) pressedKeys.add('shift');
    if (e.altKey) pressedKeys.add('alt');
    if (e.metaKey) pressedKeys.add('win');
    
    // Add main key if it's not a modifier
    if (!['control', 'shift', 'alt', 'meta'].includes(key)) {
        pressedKeys.add(key === ' ' ? 'space' : key);
    }
    
    // Build hotkey string
    const modifiers = [];
    const mainKeys = [];
    
    for (const k of pressedKeys) {
        if (['ctrl', 'shift', 'alt', 'win'].includes(k)) {
            modifiers.push(k);
        } else {
            mainKeys.push(k);
        }
    }
    
    if (mainKeys.length > 0) {
        const hotkeyStr = [...modifiers, ...mainKeys].join('+');
        hotkeyInput.value = formatHotkeyDisplay(hotkeyStr);
        
        // Validate
        await validateHotkey(hotkeyStr);
    }
});

// Validate hotkey
async function validateHotkey(hotkeyStr) {
    try {
        const response = await fetch('/api/settings/hotkey/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ hotkey: hotkeyStr })
        });
        
        const data = await response.json();
        const validation = document.getElementById('hotkeyValidation');
        const saveBtn = document.getElementById('saveHotkeyBtn');
        
        if (data.valid) {
            if (data.warning) {
                validation.style.display = 'block';
                validation.style.background = 'rgba(245, 158, 11, 0.1)';
                validation.style.border = '1px solid #f59e0b';
                validation.style.color = '#f59e0b';
                validation.textContent = '⚠️ ' + data.warning;
            } else {
                validation.style.display = 'block';
                validation.style.background = 'rgba(16, 185, 129, 0.1)';
                validation.style.border = '1px solid var(--success)';
                validation.style.color = 'var(--success)';
                validation.textContent = '✓ Valid hotkey combination';
            }
            saveBtn.disabled = false;
        } else {
            validation.style.display = 'block';
            validation.style.background = 'rgba(239, 68, 68, 0.1)';
            validation.style.border = '1px solid #ef4444';
            validation.style.color = '#ef4444';
            validation.textContent = '✗ ' + data.error;
            saveBtn.disabled = true;
        }
    } catch (error) {
        console.error('Validation error:', error);
    }
}

// Save hotkey
async function saveHotkey() {
    const hotkeyInput = document.getElementById('hotkeyInput').value;
    const hotkeyStr = hotkeyInput.toLowerCase().replace(/\s/g, '');
    
    try {
        const response = await fetch('/api/settings/hotkey', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ hotkey: hotkeyStr })
        });
        
        if (response.ok) {
            showStatus('Hotkey updated! Please restart the desktop app for changes to take effect.', 'success');
            currentHotkey = hotkeyStr;
            document.getElementById('hotkeyValidation').style.display = 'none';
        } else {
            showStatus('Failed to update hotkey', 'error');
        }
    } catch (error) {
        console.error('Save error:', error);
        showStatus('Failed to update hotkey', 'error');
    }
}

// Reset hotkey
async function resetHotkey() {
    try {
        const response = await fetch('/api/settings/hotkey/reset', {
            method: 'POST'
        });
        
        if (response.ok) {
            document.getElementById('hotkeyInput').value = 'Ctrl+Space';
            currentHotkey = 'ctrl+space';
            document.getElementById('hotkeyValidation').style.display = 'none';
            showStatus('Hotkey reset to default (Ctrl+Space)', 'success');
        }
    } catch (error) {
        console.error('Reset error:', error);
        showStatus('Failed to reset hotkey', 'error');
    }
}

// Initialize
loadSettings();
loadAutoStartStatus();
loadCurrentHotkey();
