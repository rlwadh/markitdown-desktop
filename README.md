# MarkItDown Desktop & Web v3.0

🔄 **Professional document conversion tools** - Convert files to Markdown with unlimited processing power!

[![Version](https://img.shields.io/badge/version-v3.0-blue.svg)](https://github.com/rlwadh/markitdown-desktop)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Kindergarten](https://img.shields.io/badge/supports-kindergarten%20project-red.svg)](https://www.paypal.com/donate/?hosted_button_id=PAGH54TWEXP54)

> **Zwei mächtige Versionen**: Desktop-App (Python) und Web-App (HTML) - beide mit unbegrenzter PDF-Verarbeitung und Multi-File-Support!

## 🎯 **Was ist NEU in v3.0**

### 🖥️ Desktop Version (Python)
- ✅ **Multi-File Batch-Verarbeitung** - Hunderte Dateien auf einmal konvertieren
- ✅ **ZIP-Export-Funktionalität** - Alle konvertierten Dateien in einem Archiv herunterladen
- ✅ **Ordnerstruktur beibehalten** - Ursprüngliche Verzeichnis-Struktur erhalten
- ✅ **Fortschritt-Tracking** - Echtzeitanzeige des Konvertierungsfortschritts
- ✅ **Cross-Platform** - Funktioniert auf Windows, macOS und Linux

### 🌐 Web Version (HTML) - NEU!
- ✅ **MULTIFILE FIX** - Verarbeitet jetzt ALLE ausgewählten Dateien (Single-File-Bug behoben)
- ✅ **Unbegrenzte PDF-Verarbeitung** - KEINE 10-Seiten-Begrenzung, verarbeitet komplette Dokumente
- ✅ **Drag & Drop Interface** - Einfache Dateiauswahl
- ✅ **Browser-basiert** - Keine Installation erforderlich
- ✅ **Individuelle Datei-Vorschau** - Jede konvertierte Datei einzeln prüfen

## 🚀 **Schnellstart**

### Option 1: Web Version (Sofort verwenden) - NEU!
[![Web App starten](https://img.shields.io/badge/🌐-Web%20App%20starten-blue.svg?style=for-the-badge)](https://rlwadh.github.io/markitdown-desktop/web/markitdown_v3.html)

```bash
# Datei herunterladen
curl -O https://raw.githubusercontent.com/rlwadh/markitdown-desktop/main/web/markitdown_v3.html

# In Browser öffnen - FERTIG!
```

### Option 2: Desktop Version (Erweiterte Features)
```bash
# Repository klonen
git clone https://github.com/rlwadh/markitdown-desktop.git
cd markitdown-desktop

# Desktop App starten
python desktop/markitdown_desktop_v3.py
# Abhängigkeiten werden automatisch installiert!
```

### Option 3: Nur Desktop-App herunterladen
```bash
# Windows/Linux
curl -O https://raw.githubusercontent.com/rlwadh/markitdown-desktop/main/desktop/markitdown_desktop_v3.py
python markitdown_desktop_v3.py

# macOS
curl -O https://raw.githubusercontent.com/rlwadh/markitdown-desktop/main/desktop/markitdown_desktop_v3.py
python3 markitdown_desktop_v3.py
```

## 📁 **Repository-Struktur**

```
markitdown-desktop/
├── desktop/                          # 🖥️ Python Desktop-Anwendung
│   ├── markitdown_desktop_v3.py      # Haupt-Desktop-Anwendung (NEU)
│   └── markitdown_desktop.py         # Legacy Version (v2.5)
├── web/                              # 🌐 HTML Web-Anwendung (NEU)
│   ├── markitdown_v3.html            # Haupt-Web-Anwendung
│   └── markitdown_v2.html            # Vorherige Version
├── docs/                             # 📚 Dokumentation
│   ├── CHANGELOG.md                  # Versionshistorie
│   ├── INSTALLATION.md               # Installationsanleitung
│   └── USAGE.md                      # Nutzungsanleitung
├── examples/                         # 📋 Beispieldateien
│   ├── sample.pdf
│   ├── sample.docx
│   └── sample.csv
├── screenshots/                      # 📸 Screenshots
│   ├── desktop_v3.png
│   ├── web_v3.png
│   └── comparison.png
├── README.md                         # Diese Datei
├── LICENSE                           # MIT Lizenz
└── requirements.txt                  # Python-Abhängigkeiten
```

## 📋 **Unterstützte Formate**

| Kategorie | Formate | Verarbeitung |
|-----------|---------|--------------|
| **📄 Office** | Word, Excel, PowerPoint (.docx, .xlsx, .pptx, etc.) | ✅ Vollständiger Inhalt |
| **📝 PDF** | Alle PDF-Dokumente | 🚀 **UNBEGRENZT** - Alle Seiten |
| **🖼️ Bilder** | JPG, PNG, GIF | ✅ OCR-Texterkennung |
| **🎵 Audio** | MP3, WAV | ✅ Sprach-Transkription |
| **🌐 Web** | HTML, CSV, JSON, XML | ✅ Struktur erhalten |
| **📦 Archive** | ZIP-Dateien | ✅ Inhalt-Extraktion |
| **📖 E-Books** | EPUB | ✅ Text-Extraktion |

## 🏆 **Hauptfunktionen**

### 🖥️ **Desktop Version**
- **Multi-File-Verarbeitung**: Hunderte Dateien in einem Batch konvertieren
- **ZIP-Export**: Alle Ergebnisse in organisiertem Archiv herunterladen
- **Ordner-Erhaltung**: Ursprüngliche Verzeichnisstruktur beibehalten
- **Fortschritt-Tracking**: Echtzeitanzeige des Konvertierungsfortschritts
- **Fehlerbehandlung**: Problematische Dateien überspringen und fortfahren
- **Vorschau-System**: Konvertierten Inhalt vor Export prüfen

### 🌐 **Web Version**
- **Browser-basiert**: Keine Installation erforderlich
- **Unbegrenzte PDFs**: Komplette Dokumente verarbeiten, nicht nur 10 Seiten
- **Multi-File-Support**: Mehrere Dateien auswählen und konvertieren
- **Drag & Drop**: Intuitive Dateiauswahl
- **Echtzeit-Vorschau**: Ergebnisse sofort sehen
- **Mobile-freundlich**: Funktioniert auf Tablets und Handys

## 💻 **Installation**

### Desktop Version
```bash
# Methode 1: Automatisch (Empfohlen)
python markitdown_desktop_v3.py
# Abhängigkeiten werden beim ersten Start automatisch installiert

# Methode 2: Manuell
pip install "markitdown[all]"
python markitdown_desktop_v3.py
```

### Web Version
```bash
# Keine Installation nötig!
# Einfach markitdown_v3.html herunterladen und im Browser öffnen
```

## 🎯 **Verwendungsbeispiele**

### Einzelne Datei konvertieren (Web)
1. `markitdown_v3.html` öffnen
2. PDF/Word/Excel-Datei hineinziehen
3. "Convert to Markdown" klicken
4. Ergebnis kopieren oder herunterladen

### Batch-Konvertierung mehrerer Dateien (Desktop)
1. `python markitdown_desktop_v3.py` ausführen
2. "Add Files" oder "Add Folder" klicken
3. Verarbeitungsoptionen einstellen
4. "Start Batch Processing" klicken
5. Als ZIP exportieren wenn fertig

### Große PDF verarbeiten (Beide Versionen)
- **Traditionelle Tools**: Begrenzt auf 10 Seiten
- **MarkItDown v3**: Verarbeitet ALLE Seiten ohne Limits!

## 🔧 **Versionshistorie**

| Version | Veröffentlichung | Hauptfunktionen |
|---------|------------------|-----------------|
| **v3.0** | 2024-06 | Multi-File-Support, MULTIFILE FIX, ZIP-Export, Web-Version |
| **v2.5** | 2024-06 | Emoji-Fix macOS, Cross-Platform-Kompatibilität |
| **v2.4** | 2024-06 | Vollständige GUI mit Spenden-Support |

## 🛠️ **Technische Details**

### Desktop-Anforderungen
- Python 3.7+
- tkinter (meist vorinstalliert)
- MarkItDown-Bibliothek (automatisch installiert)
- 50MB freier Speicherplatz

### Web-Anforderungen
- Moderner Browser (Chrome, Firefox, Safari, Edge)
- JavaScript aktiviert
- Kein Server erforderlich - läuft lokal

### Unterstützte Betriebssysteme
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu, Debian, etc.)

## 🎁 **Unterstützung für ein großartiges Projekt**

Dieses Projekt unterstützt ein bedeutungsvolles Kindergarten-Projekt! Der Entwickler gründet einen Kindergarten für qualitativ hochwertige frühkindliche Bildung.

**💝 Jede Spende hilft, eine liebevolle Umgebung für die Entwicklung von Kindern zu schaffen:**

[![Spenden](https://img.shields.io/badge/Spenden-PayPal-blue.svg)](https://www.paypal.com/donate/?hosted_button_id=PAGH54TWEXP54)

Deine Unterstützung macht einen echten Unterschied im Leben von Kindern! 👶🎒📚

## 👨‍💻 **Entwickler**

**Rudolf Wagner**  
🔗 [LinkedIn](https://www.linkedin.com/in/rudolfwagner)  
🎁 [Kindergarten-Projekt unterstützen](https://www.paypal.com/donate/?hosted_button_id=PAGH54TWEXP54)

## 🤝 **Mitwirken**

Beiträge sind willkommen! Bitte zögere nicht, Issues und Pull Requests einzureichen.

1. Repository forken
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Änderungen committen (`git commit -m 'Add amazing feature'`)
4. Zum Branch pushen (`git push origin feature/amazing-feature`)
5. Pull Request öffnen

## 📄 **Lizenz**

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

## 🔗 **Verwandte Projekte**

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) - Die zentrale Konvertierungs-Engine
- [PDF.js](https://github.com/mozilla/pdf.js) - PDF-Verarbeitung in der Web-Version

## 📞 **Support**

- 🐛 **Bug-Reports**: [GitHub Issues](https://github.com/rlwadh/markitdown-desktop/issues)
- 💡 **Feature-Anfragen**: [GitHub Discussions](https://github.com/rlwadh/markitdown-desktop/discussions)
- 📧 **Direkter Kontakt**: [LinkedIn](https://www.linkedin.com/in/rudolfwagner)

---

<div align="center">

**Entwickelt mit ❤️ für Dokumentenverarbeitung und 🎁 Kindergarten-Unterstützung**

[![Dieses Repo mit Stern bewerten](https://img.shields.io/github/stars/rlwadh/markitdown-desktop?style=social)](https://github.com/rlwadh/markitdown-desktop)

</div>
