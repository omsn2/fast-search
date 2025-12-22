// FilterManager - Manages search result filtering
// Supports filtering by file type, date, size, and directory

class FilterManager {
    constructor() {
        this.activeFilters = {
            fileType: null,
            dateRange: { start: null, end: null, preset: null },
            sizeRange: { min: null, max: null, preset: null },
            directory: null
        };
        
        // File type categories
        this.fileTypeCategories = {
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "Code": [".js", ".py", ".java", ".cpp", ".c", ".h", ".html", ".css", ".json", ".xml"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
            "Spreadsheets": [".xlsx", ".xls", ".csv", ".ods"],
            "Presentations": [".ppt", ".pptx", ".odp"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
            "Audio": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"]
        };
        
        // Date presets (in milliseconds)
        this.datePresets = {
            "today": 24 * 60 * 60 * 1000,           // 1 day
            "week": 7 * 24 * 60 * 60 * 1000,        // 7 days
            "month": 30 * 24 * 60 * 60 * 1000,      // 30 days
            "year": 365 * 24 * 60 * 60 * 1000       // 365 days
        };
        
        // Size presets (in bytes)
        this.sizePresets = {
            "small": { min: 0, max: 1024 * 1024 },              // < 1 MB
            "medium": { min: 1024 * 1024, max: 10 * 1024 * 1024 }, // 1-10 MB
            "large": { min: 10 * 1024 * 1024, max: Infinity }   // > 10 MB
        };
    }

    /**
     * Apply all active filters to results
     * @param {Array} results - Array of search result objects
     * @returns {Array} Filtered results
     */
    applyFilters(results) {
        if (!results || results.length === 0) {
            return results;
        }

        let filtered = [...results];

        // Apply file type filter
        if (this.activeFilters.fileType) {
            filtered = this.filterByType(filtered);
        }

        // Apply date filter
        if (this.activeFilters.dateRange.start || this.activeFilters.dateRange.end || this.activeFilters.dateRange.preset) {
            filtered = this.filterByDate(filtered);
        }

        // Apply size filter
        if (this.activeFilters.sizeRange.min !== null || this.activeFilters.sizeRange.max !== null || this.activeFilters.sizeRange.preset) {
            filtered = this.filterBySize(filtered);
        }

        // Apply directory filter
        if (this.activeFilters.directory) {
            filtered = this.filterByDirectory(filtered);
        }

        return filtered;
    }

    /**
     * Filter by file type
     * @param {Array} results - Results to filter
     * @returns {Array} Filtered results
     */
    filterByType(results) {
        const filterValue = this.activeFilters.fileType;
        
        // Check if it's a category or specific extension
        if (this.fileTypeCategories[filterValue]) {
            // It's a category
            const extensions = this.fileTypeCategories[filterValue];
            return results.filter(result => 
                extensions.includes(result.extension.toLowerCase())
            );
        } else {
            // It's a specific extension
            return results.filter(result => 
                result.extension.toLowerCase() === filterValue.toLowerCase()
            );
        }
    }

    /**
     * Filter by date modified
     * @param {Array} results - Results to filter
     * @returns {Array} Filtered results
     */
    filterByDate(results) {
        const now = Date.now() / 1000; // Current time in seconds
        let startTime = this.activeFilters.dateRange.start;
        let endTime = this.activeFilters.dateRange.end;

        // If using a preset, calculate the time range
        if (this.activeFilters.dateRange.preset) {
            const preset = this.activeFilters.dateRange.preset;
            const milliseconds = this.datePresets[preset];
            if (milliseconds) {
                startTime = now - (milliseconds / 1000);
                endTime = now;
            }
        }

        return results.filter(result => {
            const fileTime = result.modified_time || result.modifiedTime || 0;
            
            if (startTime && fileTime < startTime) {
                return false;
            }
            if (endTime && fileTime > endTime) {
                return false;
            }
            return true;
        });
    }

    /**
     * Filter by file size
     * @param {Array} results - Results to filter
     * @returns {Array} Filtered results
     */
    filterBySize(results) {
        let minSize = this.activeFilters.sizeRange.min;
        let maxSize = this.activeFilters.sizeRange.max;

        // If using a preset, use preset values
        if (this.activeFilters.sizeRange.preset) {
            const preset = this.sizePresets[this.activeFilters.sizeRange.preset];
            if (preset) {
                minSize = preset.min;
                maxSize = preset.max;
            }
        }

        return results.filter(result => {
            const fileSize = result.size || 0;
            
            if (minSize !== null && fileSize < minSize) {
                return false;
            }
            if (maxSize !== null && maxSize !== Infinity && fileSize > maxSize) {
                return false;
            }
            return true;
        });
    }

    /**
     * Filter by directory
     * @param {Array} results - Results to filter
     * @returns {Array} Filtered results
     */
    filterByDirectory(results) {
        const directory = this.activeFilters.directory.toLowerCase();
        return results.filter(result => 
            result.path.toLowerCase().includes(directory)
        );
    }

    /**
     * Set file type filter
     * @param {string} fileType - File type category or extension
     */
    setFileTypeFilter(fileType) {
        this.activeFilters.fileType = fileType;
    }

    /**
     * Set date filter using preset
     * @param {string} preset - Date preset (today, week, month, year)
     */
    setDateFilter(preset) {
        this.activeFilters.dateRange.preset = preset;
        this.activeFilters.dateRange.start = null;
        this.activeFilters.dateRange.end = null;
    }

    /**
     * Set custom date range filter
     * @param {number} start - Start timestamp (seconds)
     * @param {number} end - End timestamp (seconds)
     */
    setCustomDateRange(start, end) {
        this.activeFilters.dateRange.start = start;
        this.activeFilters.dateRange.end = end;
        this.activeFilters.dateRange.preset = null;
    }

    /**
     * Set size filter using preset
     * @param {string} preset - Size preset (small, medium, large)
     */
    setSizeFilter(preset) {
        this.activeFilters.sizeRange.preset = preset;
        this.activeFilters.sizeRange.min = null;
        this.activeFilters.sizeRange.max = null;
    }

    /**
     * Set custom size range filter
     * @param {number} min - Minimum size in bytes
     * @param {number} max - Maximum size in bytes
     */
    setCustomSizeRange(min, max) {
        this.activeFilters.sizeRange.min = min;
        this.activeFilters.sizeRange.max = max;
        this.activeFilters.sizeRange.preset = null;
    }

    /**
     * Set directory filter
     * @param {string} directory - Directory path
     */
    setDirectoryFilter(directory) {
        this.activeFilters.directory = directory;
    }

    /**
     * Clear specific filter
     * @param {string} filterType - Type of filter to clear
     */
    clearFilter(filterType) {
        switch(filterType) {
            case 'fileType':
                this.activeFilters.fileType = null;
                break;
            case 'date':
                this.activeFilters.dateRange = { start: null, end: null, preset: null };
                break;
            case 'size':
                this.activeFilters.sizeRange = { min: null, max: null, preset: null };
                break;
            case 'directory':
                this.activeFilters.directory = null;
                break;
        }
    }

    /**
     * Clear all filters
     */
    clearAllFilters() {
        this.activeFilters = {
            fileType: null,
            dateRange: { start: null, end: null, preset: null },
            sizeRange: { min: null, max: null, preset: null },
            directory: null
        };
    }

    /**
     * Get active filters as array of objects
     * @returns {Array} Array of active filter objects
     */
    getActiveFilters() {
        const active = [];

        if (this.activeFilters.fileType) {
            active.push({
                type: 'fileType',
                label: this.activeFilters.fileType,
                value: this.activeFilters.fileType
            });
        }

        if (this.activeFilters.dateRange.preset) {
            const presetLabels = {
                'today': 'Today',
                'week': 'This Week',
                'month': 'This Month',
                'year': 'This Year'
            };
            active.push({
                type: 'date',
                label: presetLabels[this.activeFilters.dateRange.preset] || this.activeFilters.dateRange.preset,
                value: this.activeFilters.dateRange.preset
            });
        }

        if (this.activeFilters.sizeRange.preset) {
            const presetLabels = {
                'small': 'Small (<1 MB)',
                'medium': 'Medium (1-10 MB)',
                'large': 'Large (>10 MB)'
            };
            active.push({
                type: 'size',
                label: presetLabels[this.activeFilters.sizeRange.preset] || this.activeFilters.sizeRange.preset,
                value: this.activeFilters.sizeRange.preset
            });
        }

        if (this.activeFilters.directory) {
            active.push({
                type: 'directory',
                label: this.activeFilters.directory,
                value: this.activeFilters.directory
            });
        }

        return active;
    }

    /**
     * Get count of active filters
     * @returns {number} Number of active filters
     */
    getActiveFilterCount() {
        return this.getActiveFilters().length;
    }

    /**
     * Check if any filters are active
     * @returns {boolean} True if any filters are active
     */
    hasActiveFilters() {
        return this.getActiveFilterCount() > 0;
    }
}
