# Quick Start Guide

## Setup (One-time)

1. **Install dependencies** (if not already done):
   ```bash
   .\venv\Scripts\python.exe -m pip install click rapidfuzz watchdog python-dateutil
   ```

2. **Index your files**:
   ```bash
   .\fast-search.bat index "C:\Users\YourName\Documents"
   ```

## Daily Usage

### Search for files
```bash
.\fast-search.bat search "your query"
```

### Examples
```bash
# Find resume
.\fast-search.bat search "resume"

# Find photos (fuzzy matching works!)
.\fast-search.bat search "phto"

# Limit results
.\fast-search.bat search "document" --limit 20
```

### View what's indexed
```bash
.\fast-search.bat stats
```

### Re-index (clear and rebuild)
```bash
.\fast-search.bat index "C:\Path\To\Folder" --clear
```

### Test performance
```bash
.\fast-search.bat benchmark "test query" --iterations 100
```

## Tips

- **Fuzzy matching**: You don't need exact spelling! Try "dcmnt" to find "document.pdf"
- **Multiple directories**: Index multiple folders by listing them:
  ```bash
  .\fast-search.bat index "C:\Projects" "D:\Work" "C:\Downloads"
  ```
- **Fast results**: Search is typically <1ms, so results appear instantly!

## Troubleshooting

### "No files indexed" error
Run the index command first:
```bash
.\fast-search.bat index "C:\Your\Folder"
```

### Path doesn't exist error
Make sure the path is correct and exists. Use quotes for paths with spaces.

### No results found
- Try a shorter query
- Check if the file is in an indexed directory
- Try fuzzy matching (partial words)

---

**Ready to search!** 🚀
