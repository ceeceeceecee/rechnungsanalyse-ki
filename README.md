# Rechnungsanalyse KI

<p align="center">
  <img src="screenshots/dashboard.png" alt="Dashboard mit Rechnungsübersicht" width="700">
</p>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python) ![DSGVO](https://img.shields.io/badge/DSGVO-Konform-brightgreen) ![Self-Hosted](https://img.shields.io/badge/Self-Hosted-blue) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker) ![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-FF4B4B?logo=streamlit) ![License](https://img.shields.io/badge/License-MIT-green)

> KI-gestützte Rechnungsprüfung mit Anomalieerkennung – DSGVO-konform, self-hosted

## Was macht die App?

Automatische Rechnungsprüfung mit KI-Unterstützung. Erkennt Anomalien, prüft Beträge und Lieferdaten, erstellt Prüfberichte. Alles self-hosted mit Ollama als lokale KI-Engine – keine Daten verlassen den Server.

## Features

- 🔍 **Automatische Rechnungserkennung** – Rechnungen hochladen und analysieren
- 🚨 **Anomalieerkennung** – Auffällige Beträge und Abweichungen sofort erkennen
- 📊 **Plausibilitätsprüfung** – KI-gestützte Prüfung der Rechnungsdaten
- 📋 **Prüfberichte** – Automatische Generierung von Prüfberichten
- 📤 **Export** – Ergebnisse als PDF/CSV exportieren
- ⚙️ **Einstellungen** – KI-Modell und Schwellenwerte konfigurieren
- 🔒 **DSGVO-konform** – Alle Daten bleiben lokal auf dem Server

## Tech Stack

| Technologie | Zweck |
|-------------|-------|
| Python 3.11+ | Backend |
| Streamlit | Web-Interface |
| Ollama | Lokale KI |
| SQLite | Datenbank |
| Docker | Deployment |

## Screenshots

**Dashboard mit Rechnungsübersicht**

<img src="screenshots/dashboard.png" alt="Dashboard" width="800">

**Rechnung scannen und analysieren**

<img src="screenshots/scannen.png" alt="Scannen" width="800">

**Analyse-Ergebnis mit Anomalien**

<img src="screenshots/ergebnisse.png" alt="Ergebnisse" width="800">

## Quick Start

### Voraussetzungen
- Docker und Docker Compose installiert
- Ollama installiert (optional, für KI-Funktionen)

### Starten

```bash
git clone https://github.com/ceeceeceecee/rechnungsanalyse-ki.git
cd rechnungsanalyse-ki
docker compose up -d
```

Die App ist dann erreichbar unter: **http://localhost:8501**

### Ohne Docker

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Konfiguration

Die App benötigt keine zusätzliche Konfiguration. Standardmäßig werden alle Daten in der SQLite-Datenbank gespeichert.

Für KI-Funktionen muss [Ollama](https://ollama.ai) installiert sein:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3
```

## License

MIT License – siehe [LICENSE](LICENSE).
