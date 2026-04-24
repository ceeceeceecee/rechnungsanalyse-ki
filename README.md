# 🧾 Rechnungsanalyse-KI – KI-gestützte Rechnungsprüfung

![DSGVO-konform](https://img.shields.io/badge/DSGVO-konform-brightgreen)
![Self_Hosted](https://img.shields.io/badge/Deployment-Self_Hosted-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB)
![Ollama](https://img.shields.io/badge/KI-Backend-Ollama-333)

## 🚨 Das Problem

Unternehmen bearbeiten täglich Hunderte von Rechnungen — manuell, fehleranfällig und langsam. Doppelzahlungen, falsche Beträge und betrügerische Rechnungen kosten deutsche Unternehmen jährlich Milliarden. Die manuelle Prüfung skaliert nicht und bindet wertvolle Ressourcen.

**Rechnungsanalyse-KI** automatisiert die Rechnungsprüfung: Datenextraktion aus PDFs, Anomalieerkennung, Dubletten-Check und Export in gängige Buchhaltungsformate.

## ✅ Features

- **🔍 Automatische Datenextraktion** — KI liest Rechnungsdaten aus PDF und Bildern (OCR)
- **⚠️ Anomalieerkennung** — Doppelrechnungen, ungewöhnliche Beträge, verdächtige Lieferanten
- **📊 Risiko-Score** — Jede Rechnung bekommt einen automatischen Risikowert (0-100)
- **📁 Export** — CSV, DATEV, SAP-kompatible Formate
- **🧠 Lokale KI (Ollama)** — DSGVO-konform, keine Datenabgabe an Cloud-Dienste
- **📈 Statistiken** — Ausgabenanalyse nach Kategorie, Lieferant, Zeitraum
- **🐳 Ein-Kommando-Install** — `docker compose up -d` und loslegen

## 🚀 Schnellstart

```bash
git clone https://github.com/ceeceeceecee/rechnungsanalyse-ki.git
cd rechnungsanalyse-ki

cp config/settings.example.yaml config/settings.yaml
docker compose up -d

open http://localhost:8501
```

## 📋 Voraussetzungen

| Komponente | Version | Zweck |
|---|---|---|
| Docker | 20.10+ | Container-Deployment |
| Docker Compose | 2.0+ | Service-Orchestrierung |
| Ollama | neueste | Lokale KI-Verarbeitung |

## 📁 Projektstruktur

```
rechnungsanalyse-ki/
├── app.py                    # Streamlit Web-App
├── processor/
│   ├── invoice_scanner.py    # Rechnungs-OCR und Datenextraktion
│   ├── anomaly_detector.py   # Anomalieerkennung
│   └── export.py             # DATEV/SAP/CSV Export
├── database/
│   ├── schema.sql            # SQLite Schema
│   └── models.py             # Datenbankzugriff
├── config/
│   └── settings.example.yaml # Konfigurations-Template
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── LICENSE
```

## ⚙️ Konfiguration

Alle Einstellungen in `config/settings.yaml`:

- **ollama_url** — URL zur lokalen Ollama-Instanz
- **model** — Genutztes LLM-Modell (empfohlen: llama3.1)
- **risk_threshold** — Schwellwert für Alarmierung bei Anomalien
- **export_format** — Standard-Exportformat (csv/datev/sap)

## 📸 Screenshots

### Dashboard — Übersicht und KPIs
![Dashboard](screenshots/dashboard.png)

### Rechnung scannen — Upload und Datenextraktion
![Scannen](screenshots/scannen.png)

### Prüfungsergebnisse — Anomalie-Report
![Ergebnisse](screenshots/ergebnisse.png)

## 📄 Lizenz

MIT License — siehe [LICENSE](LICENSE)
