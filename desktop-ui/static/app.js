// Fast Search - Desktop UI JavaScript

let searchResults = [];
let selectedIndex = -1;
let searchTimeout = null;

// DOM Elements
const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('resultsContainer');
const resultsList = document.getElementById('resultsList');
const emptyState = document.getElementById('emptyState');
const searchStats = document.getElementById('searchStats');
const indexStats = document.getElementById('indexStats');

// File type icons
const fileIcons = {
    '.pdf': '📄',
    '.doc': '📝',
    '.docx': '📝',
    '.txt': '📃',
    '.xlsx': '📊',
    '.xls': '📊',
    '.ppt': '📽️',
    '.pptx': '📽️',
    '.jpg': '🖼️',
    '.jpeg': '🖼️',
    '.png': '🖼️',
    '.gif': '🖼️',
    '.mp4': '🎬',
    '.mp3': '🎵',
    '.zip': '📦',
    '.rar': '📦',
    '.py': '🐍',
    '.js': '📜',
    '.html': '🌐',
    '.css': '🎨',
    '.json': '📋',
    '.md': '📖',
    'default': '📁'
};

// Get file icon
function getFileIcon(extension) {
    return fileIcons[extension.toLowerCase()] || fileIcons['default'];
}

// Format file size
function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Format time ago
function timeAgo(timestamp) {
    const now = Date.now() / 1000;
    const diff = now - timestamp;
    
    if (diff < 60) return 'just now';
    if (diff < 3600) return Math.floor(diff / 60) + 'm ago';
    if (diff < 86400) return Math.floor(diff / 3600) + 'h ago';
    if (diff < 2592000) return Math.floor(diff / 86400) + 'd ago';
    return new Date(timestamp * 1000).toLocaleDateString();
}

// Search files
async function searchFiles(query) {
    if (!query.trim()) {
        showEmptyState();
        return;
    }
    
    const startTime = performance.now();
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        const elapsed = (performance.now() - startTime).toFixed(1);
        
        searchResults = data.results;
        displayResults(searchResults, elapsed);
    } catch (error) {
        console.error('Search error:', error);
        showError('Search failed. Please try again.');
    }
}

// Display results
function displayResults(results, elapsed) {
    if (results.length === 0) {
        showNoResults();
        return;
    }
    
    emptyState.style.display = 'none';
    resultsList.classList.add('active');
    
    resultsList.innerHTML = results.map((result, index) => `
        <div class="result-item" data-index="${index}" 
             onclick="handleResultClick(${index}, event)"
             ondblclick="handleResultDoubleClick(${index}, event)">
            <div class="result-icon">${getFileIcon(result.extension)}</div>
            <div class="result-content">
                <div class="result-name">${escapeHtml(result.name)}</div>
                <div class="result-path">${escapeHtml(result.path)}</div>
            </div>
            <div class="result-score">${result.score.toFixed(0)}%</div>
        </div>
    `).join('');
    
    searchStats.textContent = `${results.length} results in ${elapsed}ms`;
    selectedIndex = -1;
}

// Handle result click - open file
function handleResultClick(index, event) {
    event.stopPropagation();
    selectedIndex = index;
    updateSelection();
    
    // Open file on click
    const result = searchResults[index];
    openFile(result.path);
}

// Handle result double click - open folder
function handleResultDoubleClick(index, event) {
    event.preventDefault();
    event.stopPropagation();
    const result = searchResults[index];
    openFolder(result.path);
    return false;  // Prevent any default action
}

// Show empty state
function showEmptyState() {
    emptyState.style.display = 'flex';
    resultsList.classList.remove('active');
    resultsList.innerHTML = '';
    searchStats.textContent = '';
    selectedIndex = -1;
}

// Show no results
function showNoResults() {
    emptyState.style.display = 'flex';
    emptyState.innerHTML = `
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
        </svg>
        <p>No files found</p>
        <p style="font-size: 14px; color: var(--text-muted);">Try a different search term</p>
    `;
    resultsList.classList.remove('active');
    searchStats.textContent = '0 results';
}

// Show error
function showError(message) {
    emptyState.style.display = 'flex';
    emptyState.innerHTML = `
        <p style="color: var(--warning);">⚠️ ${message}</p>
    `;
    resultsList.classList.remove('active');
}

// Select result
function selectResult(index) {
    selectedIndex = index;
    updateSelection();
}

// Update selection UI
function updateSelection() {
    const items = document.querySelectorAll('.result-item');
    items.forEach((item, index) => {
        if (index === selectedIndex) {
            item.classList.add('selected');
            item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        } else {
            item.classList.remove('selected');
        }
    });
}

// Open file
async function openFile(path) {
    try {
        const response = await fetch('/api/open-file', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ path })
        });
        
        const data = await response.json();
        if (!data.success) {
            console.error('Failed to open file:', data.error);
        }
    } catch (error) {
        console.error('Error opening file:', error);
    }
}

// Open folder
async function openFolder(path) {
    try {
        const response = await fetch('/api/open-folder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ path })
        });
        
        const data = await response.json();
        if (!data.success) {
            console.error('Failed to open folder:', data.error);
        }
    } catch (error) {
        console.error('Error opening folder:', error);
    }
}

// Load index stats
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        const fileCount = data.index?.file_count || 0;
        const cacheSize = data.query_cache?.size || 0;
        
        indexStats.textContent = `${fileCount.toLocaleString()} files indexed`;
        if (cacheSize > 0) {
            indexStats.textContent += ` • ${cacheSize} queries cached`;
        }
    } catch (error) {
        indexStats.textContent = 'Stats unavailable';
    }
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event Listeners
searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        searchFiles(e.target.value);
    }, 150); // Debounce 150ms
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (searchResults.length === 0) return;
    
    switch(e.key) {
        case 'ArrowDown':
            e.preventDefault();
            selectedIndex = Math.min(selectedIndex + 1, searchResults.length - 1);
            updateSelection();
            break;
            
        case 'ArrowUp':
            e.preventDefault();
            selectedIndex = Math.max(selectedIndex - 1, -1);
            updateSelection();
            break;
            
        case 'Enter':
            e.preventDefault();
            if (selectedIndex >= 0) {
                const result = searchResults[selectedIndex];
                if (e.ctrlKey || e.metaKey) {
                    openFolder(result.path);
                } else {
                    openFile(result.path);
                }
            }
            break;
            
        case 'Escape':
            searchInput.value = '';
            showEmptyState();
            searchInput.focus();
            break;
    }
});

// Initialize
loadStats();
searchInput.focus();

// Reload stats every 30 seconds
setInterval(loadStats, 30000);
