# Installation Guide

## 🚀 Quick Start

### Option 1: Web Version (Instant Use)
```bash
# Download and open in browser
curl -O https://raw.githubusercontent.com/rlwadh/markitdown-desktop/main/web/markitdown_v3.html
# Open in your browser - NO INSTALLATION NEEDED!
```

### Option 2: Desktop Version (Advanced Features)
```bash
# Download the desktop app
curl -O https://raw.githubusercontent.com/rlwadh/markitdown-desktop/main/desktop/markitdown_desktop_v3.py

# Run (dependencies install automatically)
python markitdown_desktop_v3.py
```

## 💻 Desktop Version Requirements

### Python
- **Python 3.7+** required
- Check version: `python --version`
- Download: https://python.org/downloads

### Auto-Installation
The desktop app automatically installs all dependencies on first run:
```bash
python markitdown_desktop_v3.py
# Dependencies install automatically!
```

### Manual Installation (if needed)
```bash
pip install "markitdown[all]"
python markitdown_desktop_v3.py
```

## 🌐 Web Version Requirements

### Browser Support
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

### Features
- **No installation required**
- **JavaScript must be enabled**
- **Works offline after loading**

## 🛠️ Troubleshooting

### Desktop Issues
```bash
# Update pip
pip install --upgrade pip

# Force reinstall
pip install --upgrade --force-reinstall "markitdown[all]"

# Windows: Install Visual C++ Build Tools
# macOS: Install Xcode Command Line Tools
xcode-select --install

# Linux: Install build essentials
sudo apt-get install build-essential
```

### Web Issues
- **Clear browser cache** if problems occur
- **Enable JavaScript** in browser settings
- **Check console** for error messages (F12)

## 🎯 First Run

### Desktop Version
1. Run: `python markitdown_desktop_v3.py`
2. **Auto-installation** starts if needed
3. **GUI opens** when ready
4. **Add files** and start converting!

### Web Version
1. **Open** `markitdown_v3.html` in browser
2. **Drag files** to upload area
3. **Click convert** - it's that simple!

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/rlwadh/markitdown-desktop/issues)
- 💡 **Questions**: [GitHub Discussions](https://github.com/rlwadh/markitdown-desktop/discussions)
- 📧 **Developer**: [Rudolf Wagner on LinkedIn](https://www.linkedin.com/in/rudolfwagner)
