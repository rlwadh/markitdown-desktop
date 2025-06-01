# 🚀 MarkItDown Desktop - Installations-Anleitung

Eine Schritt-für-Schritt Anleitung zur Installation von MarkItDown Desktop auf deinem System.

## 🎯 Schnellstart (TL;DR)

```bash
# 1. Python installieren (falls nicht vorhanden)
# 2. App herunterladen und starten:
python markitdown_desktop.py
# 3. Fertig! App installiert Dependencies automatisch
```

## 📋 Systemanforderungen

### Minimale Anforderungen
- **Python:** 3.7 oder höher
- **Betriebssystem:** Windows 10, macOS 10.12, Ubuntu 18.04 (oder neuer)
- **RAM:** 2 GB (4 GB empfohlen)
- **Speicher:** 500 MB freier Speicherplatz
- **Internet:** Für automatische Paket-Installation

### Empfohlene Konfiguration
- **Python:** 3.9 oder höher
- **RAM:** 8 GB oder mehr
- **Speicher:** 2 GB freier Speicherplatz
- **Internet:** Breitband für Audio-Transkription

## 🐍 Python Installation

### Windows

#### Option 1: Microsoft Store (Empfohlen)
1. Öffne **Microsoft Store**
2. Suche nach **"Python"**
3. Installiere **Python 3.11** (oder neuer)
4. ✅ Automatisch zu PATH hinzugefügt

#### Option 2: Python.org
1. Gehe zu https://python.org/downloads/
2. Lade **Python 3.11** herunter
3. **Wichtig:** ✅ **"Add Python to PATH"** aktivieren
4. Installiere mit Standardeinstellungen

#### Überprüfung:
```cmd
python --version
# Sollte zeigen: Python 3.11.x
```

### macOS

#### Option 1: Homebrew (Empfohlen)
```bash
# Homebrew installieren (falls nicht vorhanden)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python installieren
brew install python3
```

#### Option 2: Python.org
1. Gehe zu https://python.org/downloads/
2. Lade **Python 3.11 für macOS** herunter
3. Installiere die .pkg Datei

#### Überprüfung:
```bash
python3 --version
# Sollte zeigen: Python 3.11.x
```

### Linux (Ubuntu/Debian)

```bash
# System updaten
sudo apt update

# Python installieren
sudo apt install python3 python3-pip python3-tkinter

# Überprüfung
python3 --version
```

### Linux (CentOS/RHEL/Fedora)

```bash
# Python installieren
sudo yum install python3 python3-pip python3-tkinter
# oder für neuere Versionen:
sudo dnf install python3 python3-pip python3-tkinter
```

## 📥 MarkItDown Desktop herunterladen

### Option 1: Git Clone (Empfohlen)
```bash
# Repository klonen
git clone https://github.com/rudolfwagner/markitdown-desktop.git
cd markitdown-desktop
```

### Option 2: ZIP Download
1. Gehe zu https://github.com/rudolfwagner/markitdown-desktop
2. Klicke **"Code" → "Download ZIP"**
3. Entpacke die ZIP-Datei
4. Navigiere in den entpackten Ordner

### Option 3: Direkt-Download
```bash
# Nur die Python-Datei herunterladen
curl -O https://raw.githubusercontent.com/rudolfwagner/markitdown-desktop/main/markitdown_desktop.py
```

## 🚀 App starten

### Automatische Installation (Empfohlen)
```bash
# App starten - installiert Dependencies automatisch
python markitdown_desktop.py

# Bei macOS/Linux eventuell:
python3 markitdown_desktop.py
```

**Das war's!** Die App erkennt fehlende Pakete automatisch un
