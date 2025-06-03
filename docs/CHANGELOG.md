# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt hält sich an [Semantic Versioning](https://semver.org/lang/de/).

## [3.0.0] - 2024-06-03

### 🎉 Neue Features
- **Web-Version hinzugefügt**: Komplett neue HTML-basierte Version für Browser-Nutzung
- **Multi-File-Support**: Desktop-Version kann jetzt Hunderte Dateien in einem Batch verarbeiten
- **ZIP-Export**: Alle konvertierten Dateien in einem organisierten Archiv exportieren
- **Fortschritt-Tracking**: Echtzeitanzeige des Konvertierungsfortschritts für Batch-Operationen
- **Ordnerstruktur-Erhaltung**: Option zum Beibehalten der ursprünglichen Verzeichnisstruktur
- **Unbegrenzte PDF-Verarbeitung**: Entfernung der 10-Seiten-Begrenzung in beiden Versionen

### 🔧 Verbesserungen
- **MULTIFILE FIX**: Web-Version verarbeitet jetzt korrekt alle ausgewählten Dateien
- **Bessere Fehlerbehandlung**: Option zum Überspringen problematischer Dateien
- **Erweiterte Vorschau**: Individuelle Datei-Vorschau in beiden Versionen
- **Repository-Reorganisation**: Klare Trennung zwischen Desktop- und Web-Version
- **Verbesserte Dokumentation**: Komplett überarbeitete README und neue Installationsanleitungen

### 📁 Repository-Struktur
```
Neue Struktur:
├── desktop/                    # Python Desktop-Anwendung
│   ├── markitdown_desktop_v3.py
│   └── markitdown_desktop.py   # Legacy v2.5
├── web/                        # HTML Web-Anwendung
│   ├── markitdown_v3.html
│   └── markitdown_v2.html
├── docs/                       # Dokumentation
├── examples/                   # Beispieldateien
└── screenshots/                # App-Screenshots
```

### 🎯 Breaking Changes
- Desktop-App wurde nach `desktop/` Ordner verschoben
- Neue Web-Version erfordert modernen Browser mit JavaScript
- Einige Legacy-Funktionen wurden in v3 überarbeitet

## [2.5.0] - 2024-06-02

### 🔧 Verbesserungen
- **macOS Emoji-Fix**: Behoben von Emoji-Darstellungsproblemen auf macOS
- **Saubere, text-basierte Oberfläche**: Verbesserte Cross-Platform-Kompatibilität
- **Bessere Stabilität**: Alle Funktionalitäten beibehalten bei verbesserter Stabilität

### 🐛 Bugfixes
- Emoji-Anzeigefehler auf macOS behoben
- Cross-Platform-Kompatibilitätsprobleme gelöst
- Verbesserte Fehlerbehandlung bei Dateikonvertierung

## [2.4.0] - 2024-06-01

### 🎉 Neue Features
- **Vollständige GUI**: Komplett neue grafische Benutzeroberfläche
- **Kindergarten-Projekt Integration**: Eingebauter Spendenlink zur Unterstützung
- **Professionelle Dokumentation**: Umfassende README und Benutzerdokumentation
- **Auto-Installation**: Automatische Installation aller Abhängigkeiten beim ersten Start

### 🔧 Verbesserungen
- **Moderne UI**: Benutzerfreundliche Oberfläche mit Drag & Drop
- **Live-Vorschau**: HTML-Vorschau der Markdown-Ausgabe
- **Ein-Klick-Export**: Kopieren oder als .md-Datei speichern
- **Statistiken**: Zeilen-, Wörter- und Zeichenzählung

## [2.3.0] - 2024-05-30

### 🎉 Neue Features
- **Erweiterte Formatunterstützung**: Zusätzliche Dateiformate hinzugefügt
- **Verbesserte PDF-Verarbeitung**: Bessere Texterkennung aus PDF-Dateien
- **Audio-Transkription**: Unterstützung für MP3 und WAV mit Sprachtranskription

### 🔧 Verbesserungen
- **Bessere OCR**: Verbesserte Bilderkennung für Bilder und PDFs
- **Stabilere Konvertierung**: Weniger Fehler bei problematischen Dateien
- **Performance**: Schnellere Verarbeitung großer Dateien

## [2.2.0] - 2024-05-28

### 🎉 Neue Features
- **ZIP-Archiv-Support**: Möglichkeit, ZIP-Dateien zu verarbeiten
- **EPUB-Support**: Unterstützung für E-Book-Dateien
- **Erweiterte HTML-Verarbeitung**: Bessere Konvertierung von Webseiten

### 🔧 Verbesserungen
- **Robustere Fehlerbehandlung**: Bessere Behandlung von unbekannten Dateiformaten
- **Verbesserte Ausgabe**: Sauberere Markdown-Formatierung

## [2.1.0] - 2024-05-25

### 🎉 Neue Features
- **Cross-Platform-Support**: Offizielle Unterstützung für Windows, macOS und Linux
- **Automatische Abhängigkeits-Installation**: Keine manuelle Installation mehr nötig
- **Verbesserte Benutzerführung**: Klarere Anweisungen und Fehlermeldungen

### 🔧 Verbesserungen
- **Zuverlässigere Installation**: Bessere Behandlung von Installationsfehlern
- **Performance**: Schnellere Startzeiten
- **Benutzerfreundlichkeit**: Einfachere Bedienung

## [2.0.0] - 2024-05-22

### 🎉 Neue Features
- **GUI-Version**: Erste grafische Benutzeroberfläche mit tkinter
- **Drag & Drop**: Dateien einfach in die Anwendung ziehen
- **Live-Vorschau**: Sofortige Anzeige des konvertierten Markdown-Texts
- **Export-Funktionen**: Speichern und Kopieren der Ergebnisse

### 🔧 Verbesserungen
- **Bessere Benutzererfahrung**: Intuitive Bedienung ohne Kommandozeile
- **Visuelle Rückmeldung**: Fortschrittsanzeigen und Statusmeldungen
- **Erweiterte Formatunterstützung**: Mehr Dateiformate unterstützt

### 📚 Dokumentation
- **Umfassende README**: Vollständige Installations- und Nutzungsanleitung
- **Beispiele**: Beispieldateien zum Testen hinzugefügt

## [1.0.0] - 2024-05-20

### 🎉 Erste Veröffentlichung
- **Kommandozeilen-Interface**: Grundlegende Konvertierungsfunktionalität
- **Microsoft MarkItDown Integration**: Basiert auf Microsoft's MarkItDown-Tool
- **Grundlegende Formatunterstützung**: PDF, Word, Excel, PowerPoint
- **Python-basiert**: Einfache Installation mit pip

### 📋 Unterstützte Formate
- PDF-Dokumente
- Microsoft Office (Word, Excel, PowerPoint)
- Bilder mit OCR
- HTML und CSV-Dateien

---

## Legende

- 🎉 **Neue Features**: Neue Funktionalitäten
- 🔧 **Verbesserungen**: Verbesserungen bestehender Features
- 🐛 **Bugfixes**: Behobene Fehler
- 📚 **Dokumentation**: Dokumentations-Updates
- 📁 **Repository**: Strukturelle Änderungen
- 🎯 **Breaking Changes**: Änderungen, die bestehende Funktionalität beeinträchtigen könnten

---

**Format**: Dieses Changelog folgt den Prinzipien von [Keep a Changelog](https://keepachangelog.com/):
- Versionen werden in umgekehrter chronologischer Reihenfolge aufgelistet
- Änderungen werden nach Typ gruppiert
- Unreleased-Änderungen werden oben gehalten
- Veröffentlichungsdaten werden im Format YYYY-MM-DD angegeben
