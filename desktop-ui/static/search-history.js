// SearchHistory - Manages search history in localStorage
// Stores up to 20 most recent searches with deduplication

class SearchHistory {
    constructor(maxItems = 20) {
        this.maxItems = maxItems;
        this.storageKey = 'fast-search-history';
    }

    /**
     * Add a search to history
     * @param {string} query - The search query
     * @param {number} resultCount - Number of results returned
     */
    addSearch(query, resultCount = 0) {
        if (!query || !query.trim()) {
            return;
        }

        const trimmedQuery = query.trim();
        let history = this._loadFromStorage();

        // Remove existing entry if present (for deduplication)
        history = history.filter(item => item.query !== trimmedQuery);

        // Add new entry at the beginning
        const newEntry = {
            query: trimmedQuery,
            timestamp: Date.now(),
            resultCount: resultCount
        };

        history.unshift(newEntry);

        // Limit to maxItems
        if (history.length > this.maxItems) {
            history = history.slice(0, this.maxItems);
        }

        this._saveToStorage(history);
    }

    /**
     * Get all search history
     * @returns {Array} Array of search history objects
     */
    getHistory() {
        return this._loadFromStorage();
    }

    /**
     * Remove a specific search from history
     * @param {string} query - The search query to remove
     */
    removeSearch(query) {
        if (!query) {
            return;
        }

        let history = this._loadFromStorage();
        history = history.filter(item => item.query !== query);
        this._saveToStorage(history);
    }

    /**
     * Clear all search history
     */
    clearHistory() {
        this._saveToStorage([]);
    }

    /**
     * Load history from localStorage
     * @private
     * @returns {Array} Array of search history objects
     */
    _loadFromStorage() {
        try {
            const data = localStorage.getItem(this.storageKey);
            if (!data) {
                return [];
            }

            const parsed = JSON.parse(data);
            
            // Validate data structure
            if (!Array.isArray(parsed)) {
                console.warn('Invalid history data format, resetting');
                localStorage.removeItem(this.storageKey);
                return [];
            }

            // Validate each item has required fields
            const validated = parsed.filter(item => {
                return item && 
                       typeof item.query === 'string' && 
                       typeof item.timestamp === 'number' &&
                       typeof item.resultCount === 'number';
            });

            return validated;
        } catch (e) {
            console.error('Failed to load search history:', e);
            // Clear corrupted data
            localStorage.removeItem(this.storageKey);
            return [];
        }
    }

    /**
     * Save history to localStorage
     * @private
     * @param {Array} history - Array of search history objects
     */
    _saveToStorage(history) {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(history));
        } catch (e) {
            if (e.name === 'QuotaExceededError') {
                console.warn('localStorage quota exceeded, trimming history');
                // Keep only last 10 items and try again
                const trimmed = history.slice(0, 10);
                try {
                    localStorage.setItem(this.storageKey, JSON.stringify(trimmed));
                } catch (e2) {
                    console.error('Failed to save even trimmed history:', e2);
                }
            } else {
                console.error('Failed to save search history:', e);
            }
        }
    }

    /**
     * Get statistics about the history
     * @returns {Object} Statistics object
     */
    getStats() {
        const history = this._loadFromStorage();
        return {
            totalSearches: history.length,
            oldestSearch: history.length > 0 ? history[history.length - 1].timestamp : null,
            newestSearch: history.length > 0 ? history[0].timestamp : null,
            totalResults: history.reduce((sum, item) => sum + item.resultCount, 0)
        };
    }
}
