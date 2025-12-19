# Fast Search - Desktop UI Quick Start

## 🚀 Launch the Desktop UI

### Step 1: Start the Application
```bash
.\launch-ui.bat
```

This will:
1. Start the Flask server on port 5000
2. Open your browser to http://127.0.0.1:5000
3. Display the beautiful search interface

### Step 2: Search for Files

1. **Type in the search box** - Results appear instantly as you type
2. **Use keyboard navigation**:
   - Press `↓` to move down through results
   - Press `↑` to move up through results
   - Press `Enter` to open the selected file
   - Press `Ctrl+Enter` to open the file's folder
   - Press `Esc` to clear the search

3. **Or use your mouse**:
   - Click any result to select it
   - Click again (or press Enter) to open

## 🎨 UI Overview

### Search Bar
- Large, prominent search input at the top
- Search icon on the left
- Real-time result count and search time on the right

### Results List
- File icon (emoji) showing file type
- File name in bold
- Full file path below name
- Match score percentage on the right
- Hover effect for better visibility
- Selected item highlighted in blue

### Footer
- Shows total number of indexed files
- Displays number of cached queries
- Updates automatically every 30 seconds

### Empty State
When no search is active, you'll see:
- Large search icon
- "Start typing to search files..." message
- Keyboard shortcuts reference guide

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `↑` | Move selection up |
| `↓` | Move selection down |
| `Enter` | Open selected file |
| `Ctrl+Enter` | Show file in folder |
| `Esc` | Clear search |

## 🎯 Tips for Best Experience

### 1. **Use Fuzzy Search**
You don't need exact spelling:
- "dcmnt" will find "document.pdf"
- "rsme" will find "resume.docx"

### 2. **Keyboard Navigation is Faster**
- Keep your hands on the keyboard
- Use arrow keys to navigate
- Press Enter to open files instantly

### 3. **Check the Footer**
- See how many files are indexed
- Monitor cache performance
- Verify index is loaded

### 4. **Search as You Type**
- No need to press Enter
- Results update automatically
- 150ms debounce for smooth experience

## 🔧 Troubleshooting

### Port Already in Use
If you see "Address already in use" error:
1. Stop any running Flask servers
2. Change port in `desktop-ui/app.py` (line with `run_server(port=5000)`)
3. Restart the application

### No Results Found
1. Check if files are indexed: `.\fast-search.bat stats`
2. If index is empty, run: `.\fast-search.bat index "C:\Your\Folder"`
3. Refresh the browser page

### Files Won't Open
1. Verify the file still exists at that location
2. Check file permissions
3. Try "Show in folder" instead (Ctrl+Enter)

## 🎨 Customization

### Change Theme Colors
Edit `desktop-ui/static/style.css`:
```css
:root {
    --primary: #6366f1;  /* Change to your color */
    --bg-primary: #0f172a;  /* Background color */
}
```

### Adjust Search Debounce
Edit `desktop-ui/static/app.js`:
```javascript
searchTimeout = setTimeout(() => {
    searchFiles(e.target.value);
}, 150); // Change delay in milliseconds
```

### Change Window Size
Edit `desktop_app.py`:
```python
window = webview.create_window(
    width=800,  # Change width
    height=600,  # Change height
)
```

## 📊 What You'll See

### On First Launch
1. Flask server starts in terminal
2. Browser opens automatically
3. Search interface loads
4. Footer shows index statistics
5. Empty state with keyboard hints

### When Searching
1. Type your query
2. Results appear instantly
3. Match scores shown (0-100%)
4. File icons indicate type
5. Search time displayed (usually <1ms!)

### When Navigating
1. Arrow keys highlight results
2. Selected item has blue border
3. Smooth scrolling to keep selection visible
4. Enter key opens file immediately

## 🌟 Pro Tips

1. **Index Before First Use**
   ```bash
   .\fast-search.bat index "C:\Users\YourName\Documents"
   ```

2. **Use File Watcher for Auto-Updates**
   ```bash
   .\fast-search.bat watch "C:\Users\YourName\Documents"
   ```

3. **Keep the UI Open**
   - Leave it running in a browser tab
   - Quick access whenever you need to find files
   - Minimal resource usage

4. **Learn the Shortcuts**
   - Keyboard navigation is 10x faster than mouse
   - Muscle memory develops quickly
   - Power user workflow

## 🎉 Enjoy!

You now have a beautiful, fast, local file search tool with:
- ⚡ Sub-millisecond search
- 🎨 Modern dark interface
- ⌨️ Full keyboard control
- 📂 Instant file access
- 🔒 Complete privacy (local only)

Happy searching! 🚀
