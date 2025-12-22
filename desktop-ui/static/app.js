// Fast Search - Desktop UI JavaScript

let searchResults = [];
let selectedIndex = -1;
let searchTimeout = null;
let lastSearchTime = 0;

// Initialize Search History
const searchHistory = new SearchHistory();

// Initialize Filter Manager
const filterManager = new FilterManager();

// DOM Elements
const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('resultsContainer');
const resultsList = document.getElementById('resultsList');
const emptyState = document.getElementById('emptyState');
const searchStats = document.getElementById('searchStats');
const indexStats = document.getElementById('indexStats');
const historyDropdown = document.getElementById('searchHistoryDropdown');
const historyList = document.getElementById('historyList');
const clearAllHistoryBtn = document.getElementById('clearAllHistory');

// Filter Panel Elements
const filterPanel = document.getElementById('filterPanel');
const filterHeader = document.getElementById('filterHeader');
const toggleFiltersBtn = document.getElementById('toggleFiltersBtn');
const filterControls = document.getElementById('filterControls');
const fileTypeFilter = document.getElementById('fileTypeFilter');
const dateFilter = document.getElementById('dateFilter');
const sizeFilter = document.getElementById('sizeFilter');
const clearFiltersBtn = document.getElementById('clearFiltersBtn');
const activeFiltersContainer = document.getElementById('activeFilters');
const filterCount = document.getElementById('filterCount');

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
        lastSearchTime = elapsed;
        
        searchResults = data.results;
        
        // Apply active filters
        const filteredResults = filterManager.applyFilters(searchResults);
        
        displayResults(filteredResults, elapsed, searchResults.length);
        
        // Add to search history
        if (query.trim()) {
            searchHistory.addSearch(query.trim(), filteredResults.length);
        }
    } catch (error) {
        console.error('Search error:', error);
        showError('Search failed. Please try again.');
    }
}

// Display results
function displayResults(results, elapsed, totalCount = null) {
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
    
    // Show filter info if filters are active
    if (totalCount && totalCount !== results.length) {
        searchStats.textContent = `${results.length} of ${totalCount} results in ${elapsed}ms`;
    } else {
        searchStats.textContent = `${results.length} results in ${elapsed}ms`;
    }
    
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

// ===== Search History Functions =====

// Display search history dropdown
function displaySearchHistory() {
    const history = searchHistory.getHistory();
    
    if (history.length === 0) {
        historyList.innerHTML = '<div class="history-empty">No recent searches</div>';
    } else {
        historyList.innerHTML = history.map(item => {
            const escapedQuery = escapeHtml(item.query);
            // Use data attribute to avoid issues with quotes in onclick
            return `
                <div class="history-item" data-query="${escapedQuery}">
                    <div class="history-item-content">
                        <div class="history-query">${escapedQuery}</div>
                        <div class="history-meta">
                            ${item.resultCount} result${item.resultCount !== 1 ? 's' : ''} • ${timeAgo(item.timestamp / 1000)}
                        </div>
                    </div>
                    <button class="history-remove-btn" data-query="${escapedQuery}" title="Remove">✕</button>
                </div>
            `;
        }).join('');
        
        // Add event listeners to history items
        document.querySelectorAll('.history-item').forEach(item => {
            item.addEventListener('click', (e) => {
                // Don't trigger if clicking the remove button
                if (!e.target.classList.contains('history-remove-btn')) {
                    const query = item.getAttribute('data-query');
                    handleHistoryClick(query);
                }
            });
        });
        
        // Add event listeners to remove buttons
        document.querySelectorAll('.history-remove-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const query = btn.getAttribute('data-query');
                handleRemoveHistory(query);
            });
        });
    }
    
    historyDropdown.classList.add('active');
}

// Hide search history dropdown
function hideSearchHistory() {
    historyDropdown.classList.remove('active');
}

// Handle history item click - re-run search
function handleHistoryClick(query) {
    searchInput.value = query;
    hideSearchHistory();
    searchFiles(query);
}

// Handle remove single history item
function handleRemoveHistory(query) {
    searchHistory.removeSearch(query);
    displaySearchHistory();
}

// Handle clear all history
function handleClearAllHistory() {
    if (confirm('Clear all search history?')) {
        searchHistory.clearHistory();
        displaySearchHistory();
    }
}

// ===== Filter Functions =====

// Toggle filter panel
function toggleFilterPanel() {
    filterPanel.classList.toggle('expanded');
}

// Handle filter change
function handleFilterChange(filterType, value) {
    switch(filterType) {
        case 'fileType':
            if (value) {
                filterManager.setFileTypeFilter(value);
            } else {
                filterManager.clearFilter('fileType');
            }
            break;
        case 'date':
            if (value) {
                filterManager.setDateFilter(value);
            } else {
                filterManager.clearFilter('date');
            }
            break;
        case 'size':
            if (value) {
                filterManager.setSizeFilter(value);
            } else {
                filterManager.clearFilter('size');
            }
            break;
    }
    
    // Re-apply filters to current results
    applyCurrentFilters();
}

// Apply filters to current results
function applyCurrentFilters() {
    if (searchResults.length === 0) return;
    
    const filtered = filterManager.applyFilters(searchResults);
    displayResults(filtered, lastSearchTime, searchResults.length);
    displayActiveFilters();
    updateFilterCount();
}

// Display active filter chips
function displayActiveFilters() {
    const activeFilters = filterManager.getActiveFilters();
    
    if (activeFilters.length === 0) {
        activeFiltersContainer.innerHTML = '';
        return;
    }
    
    activeFiltersContainer.innerHTML = activeFilters.map(filter => `
        <div class="filter-chip">
            <span>${escapeHtml(filter.label)}</span>
            <button class="filter-chip-remove" 
                    data-filter-type="${filter.type}" 
                    title="Remove filter">✕</button>
        </div>
    `).join('');
    
    // Add event listeners to remove buttons
    document.querySelectorAll('.filter-chip-remove').forEach(btn => {
        btn.addEventListener('click', () => {
            const filterType = btn.getAttribute('data-filter-type');
            removeFilter(filterType);
        });
    });
}

// Remove individual filter
function removeFilter(filterType) {
    filterManager.clearFilter(filterType);
    
    // Reset corresponding UI control
    switch(filterType) {
        case 'fileType':
            fileTypeFilter.value = '';
            break;
        case 'date':
            dateFilter.value = '';
            break;
        case 'size':
            sizeFilter.value = '';
            break;
    }
    
    applyCurrentFilters();
}

// Clear all filters
function clearAllFilters() {
    filterManager.clearAllFilters();
    
    // Reset all UI controls
    fileTypeFilter.value = '';
    dateFilter.value = '';
    sizeFilter.value = '';
    
    applyCurrentFilters();
}

// Update filter count badge
function updateFilterCount() {
    const count = filterManager.getActiveFilterCount();
    filterCount.textContent = count > 0 ? count : '';
    
    // Enable/disable clear button
    clearFiltersBtn.disabled = count === 0;
}

// Event Listeners
searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    
    // Hide history when typing
    if (e.target.value.trim()) {
        hideSearchHistory();
    }
    
    searchTimeout = setTimeout(() => {
        searchFiles(e.target.value);
    }, 150); // Debounce 150ms
});

// Show history when input is focused and empty
searchInput.addEventListener('focus', () => {
    if (!searchInput.value.trim()) {
        displaySearchHistory();
    }
});

// Hide history when clicking outside
document.addEventListener('click', (e) => {
    const searchContainer = document.querySelector('.search-container');
    if (!searchContainer.contains(e.target)) {
        hideSearchHistory();
    }
});

// Clear all history button
clearAllHistoryBtn.addEventListener('click', handleClearAllHistory);

// Filter panel toggle
filterHeader.addEventListener('click', toggleFilterPanel);
toggleFiltersBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent double toggle from header click
});

// Filter controls
fileTypeFilter.addEventListener('change', (e) => {
    handleFilterChange('fileType', e.target.value);
});

dateFilter.addEventListener('change', (e) => {
    handleFilterChange('date', e.target.value);
});

sizeFilter.addEventListener('change', (e) => {
    handleFilterChange('size', e.target.value);
});

// Clear all filters
clearFiltersBtn.addEventListener('click', clearAllFilters);

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
            hideSearchHistory();
            searchInput.focus();
            break;
    }
});

// Initialize
loadStats();
searchInput.focus();

// Reload stats every 30 seconds
setInterval(loadStats, 30000);
