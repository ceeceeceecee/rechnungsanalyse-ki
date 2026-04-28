# Rechnungsanalyse Ki

<p align="center">
</p>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python) ![DSGVO](https://img.shields.io/badge/DSGVO-Konform-brightgreen) ![Self-Hosted](https://img.shields.io/badge/Self-Hosted-blue) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker) ![Ollama](https://img.shields.io/badge/Ollama-KI-333?logo=ollama)

> KI-gestützte Rechnungsprüfung mit Anomalieerkennung (DSGVO-konform)

## Overview

Automatische Rechnungsprüfung mit KI-Unterstützung. Erkennt Anomalien, prüft Beträge und Lieferdaten, erstellt Prüfberichte. Self-hosted mit Ollama, DSGVO-konform.

## Features

- Automatische Rechnungserkennung
- Anomalieerkennung bei Beträgen
- Lieferdaten-Prüfung
- KI-gestützte Plausibilitätsprüfung
- Prüfbericht-Generierung
- DSGVO-konforme Verarbeitung

## Tech Stack

| Tech | Zweck |
|------|-------|
| Python 3.11+ | Backend |
| Streamlit | Web-Interface |
| Ollama | Lokale KI |
| SQLite | Datenbank |
| Docker | Deployment |

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Screenshots

**Dashboard mit Rechnungsübersicht**

<img src="screenshots/dashboard.png" alt="Dashboard mit Rechnungsübersicht" width="800">

**Rechnung scannen und analysieren**

<img src="screenshots/scannen.png" alt="Rechnung scannen und analysieren" width="800">

**Analyse-Ergebnis mit Anomalien**

<img src="screenshots/ergebnisse.png" alt="Analyse-Ergebnis mit Anomalien" width="800">

---

## Contributing

Beiträge sind willkommen! Bitte erstelle einen Issue oder Pull Request.

## License

MIT License — siehe [LICENSE](LICENSE).

<p align="center">
</p>