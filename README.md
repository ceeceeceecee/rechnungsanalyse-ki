# 🧾 Rechnungsanalyse-KI

**KI-gestützte Rechnungsprüfung mit automatischer Anomalieerkennung**

![DSGVO-konform](https://img.shields.io/badge/DSGVO-konform-brightgreen)
![Self_Hosted](https://img.shields.io/badge/Deployment-Self_Hosted-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB)
![Ollama](https://img.shields.io/badge/KI-Backend-Ollama-333)

---

## 🚨 Das Problem

Unternehmen bearbeiten täglich Hunderte von Rechnungen — manuell, fehleranfällig und langsam. Doppelzahlungen, falsche Beträge und betrügerische Rechnungen kosten deutsche Unternehmen jährlich Milliarden. Die manuelle Prüfung skaliert nicht und bindet wertvolle Ressourcen.

**Rechnungsanalyse-KI** automatisiert den gesamten Prüfprozess: Datenextraktion aus PDFs und Bildern, intelligente Anomalieerkennung, Dubletten-Check und direkter Export in gängige Buchhaltungsformate.

## 🎯 Zielgruppe

- **Mittelständische Unternehmen** mit hohem Rechnungsvolumen
- **Buchhaltungsabteilungen** die manuelle Prüfungen reduzieren wollen
- **Steuerberater** die mehrere Mandanten betreuen
- **Compliance-Teams** mit Fokus auf Betrugprävention

## ✅ Features

### 🔍 Automatische Datenextraktion
Die KI liest Rechnungsdaten aus PDF und Bildern (OCR) und strukturiert sie automatisch:
- Lieferant, Rechnungsnummer, Datum, Fälligkeitsdatum
- Netto-/Bruttobeträge, Mehrwertsteuer
- Einzelpositionen, IBAN/BIC, Referenznummern

### ⚠️ Intelligente Anomalieerkennung
Jede Rechnung wird automatisch auf Auffälligkeiten geprüft:
- **Dubletten-Erkennung** — Gleiche Rechnungsnummer oder Betrag bereits vorhanden?
- **Betragsanomalie** — Liegt der Betrag signifikant über dem Durchschnitt des Lieferanten?
- **Neuer Lieferant** — Unbekannter Lieferant ohne Historie?
- **Fälligkeits-Check** — Ist die Zahlung bereits überfällig?

### 📊 Risiko-Score
Jede geprüfte Rechnung erhält einen automatischen Risikowert (0–100):
- 🟢 **0–39**: Normaler Rahmen — keine Auffälligkeiten
- 🟡 **40–69**: Erhöhte Aufmerksamkeit — Einzelne Warnhinweise
- 🔴 **70–100**: Kritisch — Mehrere Anomalien, manuelle Prüfung erforderlich

### 📁 Export-Formate
Geprüfte Rechnungen direkt in Buchhaltungssoftware importieren:
- **CSV** — Universell, für alle Systeme
- **DATEV** — Kompatibel mit DATEV Unternehmen online (EXTF-Format)
- **SAP** — SAP-kompatibler Import

### 🧠 Lokale KI (Ollama)
- **100% DSGVO-konform** — Keine Datenabgabe an Cloud-Dienste
- **Lokale Verarbeitung** — Alle Daten bleiben im Unternehmen
- **Anpassbar** — Frei wählbares LLM-Modell (empfohlen: Llama 3.1)

### 🐳 Ein-Kommando-Installation
```bash
docker compose up -d
```
Fertig. Kein kompliziertes Setup, keine externen Abhängigkeiten.

## 🚀 Schnellstart

### Voraussetzungen

| Komponente | Version | Zweck |
|---|---|---|
| Docker | 20.10+ | Container-Deployment |
| Docker Compose | 2.0+ | Service-Orchestrierung |
| Ollama | neueste | Lokale KI-Verarbeitung |

### Installation

```bash
# Repo klonen
git clone https://github.com/ceeceeceecee/rechnungsanalyse-ki.git
cd rechnungsanalyse-ki

# Konfiguration kopieren
cp config/settings.example.yaml config/settings.yaml

# Empfohlenes Ollama-Modell herunterladen
docker compose run ollama pull llama3.1

# starten
docker compose up -d

# Browser öffnen
open http://localhost:8501
```

### Erste Schritte

1. **Rechnung hochladen** — PDF oder Bild per Drag & Drop
2. **KI-Analyse** — Automatische Datenextraktion und Anomalie-Check
3. **Ergebnis prüfen** — Risiko-Score und Detailbericht
4. **Speichern oder Exportieren** — In Datenbank archivieren oder als DATEV/SAP exportieren

## 📁 Projektstruktur

```
rechnungsanalyse-ki/
├── app.py                          # Streamlit Web-App (5 Seiten)
├── processor/
│   ├── invoice_scanner.py          # Rechnungs-OCR und Datenextraktion
│   ├── anomaly_detector.py         # Anomalieerkennung (Dubletten, Beträge, etc.)
│   └── export.py                   # DATEV/SAP/CSV Export
├── database/
│   ├── schema.sql                  # SQLite Schema (Invoices, Vendors, Export-Log)
│   └── models.py                   # Datenbank-Zugriffsschicht
├── config/
│   └── settings.example.yaml       # Konfigurations-Template
├── screenshots/                    # App-Screenshots
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── LICENSE
```

## 📸 Screenshots

### Dashboard — Übersicht und KPIs
![Dashboard](screenshots/dashboard.png)

### Rechnung scannen — Upload und Datenextraktion
![Scannen](screenshots/scannen.png)

### Prüfungsergebnisse — Anomalie-Report
![Ergebnisse](screenshots/ergebnisse.png)

## ⚙️ Konfiguration

Alle Einstellungen in `config/settings.yaml`:

| Einstellung | Standard | Beschreibung |
|---|---|---|
| `ollama.url` | `http://localhost:11434` | URL zur lokalen Ollama-Instanz |
| `ollama.model` | `llama3.1` | Genutztes LLM-Modell |
| `anomaly_detection.risk_threshold` | `70` | Schwellwert für kritische Anomalien |
| `anomaly_detection.check_duplicates` | `true` | Dubletten-Erkennung aktiv/inaktiv |
| `anomaly_detection.amount_variance_percent` | `20` | Max. erlaubte Betragsabweichung (%) |
| `export.default_format` | `csv` | Standard-Exportformat (csv/datev/sap) |
| `database.path` | `data/rechnungsanalyse.db` | SQLite Datenbankpfad |

## 🛠️ Tech Stack

| Technologie | Einsatz |
|---|---|
| **Python 3.11+** | Backend-Logik, Datenverarbeitung |
| **Streamlit** | Web-Oberfläche (Dashboard, Scanner, Export) |
| **Ollama** | Lokale KI für OCR und Textanalyse |
| **SQLite** | Datenspeicherung (Rechnungen, Lieferanten) |
| **Docker** | Container-Deployment |
| **Plotly** | Visualisierungen und Charts |

## 🔒 Datenschutz & Sicherheit

Rechnungsanalyse-KI ist speziell für den Einsatz in deutschen Unternehmen entwickelt:

- **DSGVO-konform** — Alle Daten werden lokal verarbeitet, keine Cloud-Übertragung
- **Keine externen APIs** — Ollama läuft vollständig auf dem eigenen Server
- **Löschkonzept** — Automatische Bereinigung alter Daten konfigurierbar
- **Zugriffskontrolle** — Streamlit-Authentifizierung optional integrierbar
- **Audit-Log** — Alle Prüfungen und Exporte werden protokolliert

## 📄 Lizenz

MIT License — siehe [LICENSE](LICENSE)

---

**Entwickelt von [Chris Cole](https://github.com/ceeceeceecee) — AI & Automation Freelancer**
