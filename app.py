"""
Rechnungsanalyse-KI — Streamlit Web-App
KI-gestützte Rechnungsprüfung mit Anomalieerkennung
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from database.models import get_connection, init_db
from processor.invoice_scanner import extract_invoice_data
from processor.anomaly_detector import check_anomalies
from processor.export import export_invoices

# -- Unified Theme System --
import sys, os as _theme_os
sys.path.insert(0, _theme_os.path.dirname(_theme_os.path.abspath(__file__)))
from theme import init_theme, theme_toggle_sidebar, app_footer


def init():
    """Initialisiere Datenbank und Session State."""
    init_db()
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"


def main():
    init()
    st.set_page_config(
        page_title="Rechnungsanalyse-KI",
        page_icon="🧾",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_theme()

    # Sidebar
    with st.sidebar:
        st.title("🧾 Rechnungsanalyse-KI")
        st.caption("Automatische Rechnungsprüfung")
        pages = ["Dashboard", "Rechnung scannen", "Prüfungsergebnisse", "Export", "Einstellungen"]
        st.session_state.page = st.radio("Navigation", pages, key="nav")
        st.divider()
        st.caption("KI: Ollama")
        st.caption("DB: Verbunden")
        st.caption("v1.0.0 | MIT License")

    # Routing
    if st.session_state.page == "dashboard":
        show_dashboard()
    elif st.session_state.page == "Rechnung scannen":
        show_scanner()
    elif st.session_state.page == "Prüfungsergebnisse":
        show_results()
    elif st.session_state.page == "Export":
        show_export()
    elif st.session_state.page == "Einstellungen":
        show_settings()


def show_dashboard():
    """Dashboard mit KPIs und Übersicht."""
    st.header("📊 Dashboard")
    conn = get_connection()
    cur = conn.cursor()

    # KPIs
    cur.execute("SELECT COUNT(*) FROM invoices WHERE status = 'geprueft'")
    total = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM invoices WHERE risk_score >= 70")
    flagged = cur.fetchone()[0] or 0
    cur.execute("SELECT COALESCE(SUM(amount), 0) FROM invoices")
    total_amount = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM invoices WHERE status = 'anomalie'")
    anomalies = cur.fetchone()[0] or 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Gesamt geprüft", total)
    col2.metric("Flaggiert", flagged, delta=f"{flagged} Risiken")
    col3.metric("Gesamtbetrag", f"€{total_amount:,.2f}")
    col4.metric("Anomalien", anomalies)

    st.divider()

    # Letzte Rechnungen
    st.subheader("Letzte Prüfungen")
    cur.execute("""
        SELECT id, vendor, invoice_number, amount, risk_score, status, created_at
        FROM invoices ORDER BY created_at DESC LIMIT 10
    """)
    rows = cur.fetchall()
    if rows:
        for row in rows:
            risk_color = "🔴" if row[4] >= 70 else ("🟡" if row[4] >= 40 else "🟢")
            st.markdown(
                f"{risk_color} **{row[1]}** — {row[2]} | "
                f"€{row[3]:,.2f} | Risiko: {row[4]}/100 | {row[5]}"
            )
    else:
        st.info("Noch keine Rechnungen geprüft. Starten Sie mit 'Rechnung scannen'.")

    conn.close()


def show_scanner():
    """Rechnung hochladen und scannen."""
    st.header("🔍 Rechnung scannen")

    with st.expander("ℹ️ So funktioniert's"):
        st.markdown(
            "Laden Sie eine Rechnung (PDF oder Bild) hoch. Die KI extrahiert automatisch "
            "Lieferant, Rechnungsnummer, Betrag, Datum und prüft auf Anomalien."
        )

    uploaded = st.file_uploader(
        "Rechnung hochladen",
        type=["pdf", "png", "jpg", "jpeg"],
        help="PDF oder Bilddatei der Rechnung"
    )

    if uploaded:
        with st.spinner("Analyse läuft..."):
            data = extract_invoice_data(uploaded)
            anomalies = check_anomalies(data)

        st.success("Analyse abgeschlossen!")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Extrahierte Daten")
            st.json(data)

        with col2:
            st.subheader("Anomalie-Check")
            if anomalies["found"]:
                for a in anomalies["details"]:
                    severity = "🔴" if a["severity"] == "high" else ("🟡" if a["severity"] == "medium" else "🟢")
                    st.markdown(f"{severity} **{a['type']}**: {a['description']}")
            else:
                st.markdown("🟢 Keine Anomalien erkannt.")

        if st.button("In Datenbank speichern"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO invoices (vendor, invoice_number, amount, invoice_date,
                    risk_score, status, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("vendor", "Unbekannt"),
                data.get("invoice_number", ""),
                data.get("amount", 0),
                data.get("invoice_date", ""),
                anomalies["risk_score"],
                "anomalie" if anomalies["found"] else "ok",
                json.dumps(data),
            ))
            conn.commit()
            conn.close()
            st.success("Gespeichert!")


def show_results():
    """Prüfungsergebnisse anzeigen."""
    st.header("📋 Prüfungsergebnisse")

    conn = get_connection()
    cur = conn.cursor()

    # Filter
    status_filter = st.selectbox(
        "Status filtern",
        ["Alle", "ok", "anomalie", "geprueft"]
    )

    query = "SELECT * FROM invoices"
    if status_filter != "Alle":
        query += f" WHERE status = '{status_filter}'"
    query += " ORDER BY risk_score DESC"

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    if rows:
        for row in rows:
            with st.expander(f"{'🔴' if row[5] >= 70 else '🟡' if row[5] >= 40 else '🟢'} "
                             f"{row[1]} — {row[2]} (€{row[3]:,.2f})"):
                st.write(f"**Risiko-Score:** {row[5]}/100")
                st.write(f"**Status:** {row[6]}")
                raw = json.loads(row[7]) if isinstance(row[7], str) else row[7]
                st.json(raw)
    else:
        st.info("Keine Ergebnisse gefunden.")


def show_export():
    """Export-Interface."""
    st.header("📁 Export")

    export_format = st.selectbox("Format", ["csv", "datev", "sap"])
    date_from = st.date_input("Von", datetime.now() - timedelta(days=30))
    date_to = st.date_input("Bis", datetime.now())

    if st.button("Exportieren"):
        data = export_invoices(export_format, date_from, date_to)
        st.download_button(
            label=f"Download {export_format.upper()}",
            data=data,
            file_name=f"rechnungen_{date_from}_{date_to}.{export_format}",
        )


def show_settings():
    """Einstellungen."""
    st.header("⚙️ Einstellungen")

    tab1, tab2 = st.tabs(["KI-Backend", "System"])

    with tab1:
        st.subheader("KI-Backend konfigurieren")
        st.info("Ollama ist das Standard-Backend (DSGVO-konform, lokal).")

        ollama_url = st.text_input("Ollama URL", value="http://localhost:11434")
        ollama_model = st.text_input("Ollama Modell", value="llama3.1")

        risk_threshold = st.slider("Risiko-Schwellwert", 0, 100, value=70)

        if st.button("Ollama testen"):
            try:
                import http.client
                conn = http.client.HTTPConnection(
                    ollama_url.replace("http://", "").split(":")[0],
                    int(ollama_url.split(":")[-1]) if ":" in ollama_url else 11434
                )
                conn.request("GET", "/api/tags")
                resp = conn.getresponse()
                if resp.status == 200:
                    st.success("Ollama erreichbar!")
                else:
                    st.error(f"Ollama Fehler: {resp.status}")
                conn.close()
            except Exception as e:
                st.error(f"Verbindung fehlgeschlagen: {e}")

    with tab2:
        st.subheader("System")
        st.text_input("Standard-Exportformat", value="csv")


if __name__ == "__main__":
    main()

# -- Theme Toggle --
theme_toggle_sidebar()

# -- Footer --
app_footer()
