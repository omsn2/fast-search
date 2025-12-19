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

// Initialize
loadSettings();
loadAutoStartStatus();
