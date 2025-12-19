# Fast Search - Lightning-Fast Local Desktop Search

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A **professional, privacy-first desktop search application** for Windows with sub-millisecond search speed, beautiful UI, and full system integration.

![Fast Search Demo](docs/demo.gif)

## ✨ Features

### 🚀 Performance
- ⚡ **Sub-1ms Search**: 100x faster than target (cached queries <0.1ms)
- 💾 **In-Memory Caching**: LRU cache for instant results
- 👁️ **Real-Time Monitoring**: Auto-updates when files change
- 📊 **Smart Indexing**: Incremental updates, no full re-scans

### 🎨 User Interface
- 🌙 **Modern Dark Theme**: Beautiful, professional design
- ⌨️ **Keyboard-First**: Full navigation with arrow keys
- 🖼️ **File Type Icons**: Visual indicators for 15+ file types
- ✨ **Smooth Animations**: Polished, responsive interactions

### 🔧 System Integration
- 🖼️ **System Tray**: Runs in background with tray icon
- ⚡ **Global Hotkey**: Press `Ctrl+Space` from anywhere
- 🚀 **Auto-Start**: Optionally start with Windows
- 📂 **File Operations**: Open files/folders with one click

### 🔒 Privacy & Control
- 🏠 **100% Local**: No cloud, no tracking, no internet required
- 🎯 **User-Controlled**: Choose which directories to index
- 🛡️ **Auto-Exclusions**: System folders automatically excluded
- 🔐 **Your Data Stays Yours**: Complete privacy

## 📸 Screenshots

### Search Interface
![Search Interface](docs/screenshot-search.png)

### Settings Page
![Settings Page](docs/screenshot-settings.png)

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Windows 10/11** (tested on Windows 11)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/fast-search.git
cd fast-search
```

2. **Create virtual environment**:
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Index your files** (first time):
```bash
python main.py index "C:\Users\YourName\Documents"
```

5. **Launch the app**:
```bash
.\launch-desktop-app.bat
```

That's it! Press `Ctrl+Space` to search! 🎉

## 📖 Usage

### Desktop App (Recommended)
```bash
.\launch-desktop-app.bat
```

**Features**:
- System tray icon
- Global hotkey (`Ctrl+Space`)
- Auto-start capability
- Background operation

### Web UI Only
```bash
.\launch-ui.bat
```

**Features**:
- Browser-based interface
- All search features
- Settings management

### CLI
```bash
.\fast-search.bat search "query"
.\fast-search.bat stats
.\fast-search.bat watch "C:\Path"
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Space` | Open search (global) |
| `↑` `↓` | Navigate results |
| `Enter` | Open selected file |
| `Ctrl+Enter` | Show in folder |
| `Esc` | Clear search |

## ⚙️ Configuration

### Add Directories to Index
1. Click **⚙️ Settings**
2. Enter directory path
3. Click **Add Directory**
4. Files are indexed automatically

### Enable Auto-Start
1. Go to **Settings**
2. Scroll to **Startup & Shortcuts**
3. Check **Start with Windows**

### Excluded Directories
System folders are automatically excluded:
- `$Recycle.Bin`, `Windows.old`
- `AppData`, `ProgramData`
- `node_modules`, `.git`, `__pycache__`
- And more...

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│     Desktop App (Python)            │
│  - System Tray (pystray)            │
│  - Global Hotkey (keyboard)         │
│  - Auto-Start (winreg)              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Flask API Server                 │
│  - Search endpoints                  │
│  - Settings management               │
│  - File operations                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Search Service                   │
│  - Index Cache (in-memory)           │
│  - Query Cache (LRU)                 │
│  - File Watcher (watchdog)           │
│  - Search Engine (RapidFuzz)         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     SQLite Database                  │
│  - File metadata                     │
│  - Optimized indexes                 │
└──────────────────────────────────────┘
```

## 🛠️ Technology Stack

- **Backend**: Python 3.10+
- **Database**: SQLite
- **Search**: RapidFuzz (fuzzy matching)
- **File Watching**: Watchdog
- **Web Framework**: Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **System Integration**: pystray, keyboard, Pillow

## 📊 Performance

| Metric | Result |
|--------|--------|
| **Search Speed** | <1ms (100x faster than target!) |
| **Cached Search** | <0.1ms |
| **Memory Usage** | ~50MB |
| **CPU (Idle)** | <1% |
| **Files Indexed** | Tested with 14,000+ files |

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md)
- [UI Guide](UI_QUICKSTART.md)
- [Phase 1: Core Engine](PHASE1_COMPLETE.md)
- [Phase 2: Performance](PHASE2_COMPLETE.md)
- [Phase 3: Desktop UI](PHASE3_COMPLETE.md)
- [Phase 4: System Integration](PHASE4_COMPLETE.md)
- [Complete Project Summary](PROJECT_SUMMARY.md)

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Test Phase 2 features:
```bash
python test_phase2.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **RapidFuzz** for lightning-fast fuzzy matching
- **Watchdog** for file system monitoring
- **Flask** for the web framework
- **pystray** for system tray integration

## 🐛 Known Issues

- Global hotkey requires administrator rights on some systems
- Auto-start only works on Windows (by design)

## 🔮 Future Enhancements

- [ ] Customizable hotkey
- [ ] File previews (thumbnails)
- [ ] Recent searches history
- [ ] Light theme option
- [ ] Multi-language support
- [ ] Cross-platform support (macOS, Linux)

## 📞 Support

If you encounter any issues or have questions:
- Open an [Issue](https://github.com/yourusername/fast-search/issues)
- Check the [Documentation](docs/)
- Read the [FAQ](docs/FAQ.md)

## ⭐ Show Your Support

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ by [Your Name]**

*Fast, Private, Local Desktop Search*
