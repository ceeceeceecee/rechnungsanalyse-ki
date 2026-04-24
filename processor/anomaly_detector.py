"""Anomalieerkennung für Rechnungen."""
from database.models import get_connection


def check_anomalies(invoice_data):
    """
    Prüfe Rechnung auf Anomalien.
    Returns dict mit found, risk_score, details.
    """
    anomalies = []
    risk_score = 0

    # 1. Dubletten-Check
    if _is_duplicate(invoice_data):
        anomalies.append({
            "type": "Dublette",
            "severity": "high",
            "description": "Rechnung mit gleicher Nummer und Lieferant existiert bereits",
        })
        risk_score += 40

    # 2. Betrags-Check (unüblich hoher Betrag)
    amount = invoice_data.get("amount", 0)
    avg = _get_average_amount(invoice_data.get("vendor", ""))
    if avg and amount > avg * 1.5:
        anomalies.append({
            "type": "Betragsanomalie",
            "severity": "medium",
            "description": f"Betrag €{amount:,.2f} liegt {((amount/avg)-1)*100:.0f}% über dem Durchschnitt (€{avg:,.2f})",
        })
        risk_score += 25

    # 3. Fälligkeits-Check
    due_date = invoice_data.get("due_date", "")
    if due_date and _is_overdue(due_date):
        anomalies.append({
            "type": "Überfällig",
            "severity": "medium",
            "description": f"Rechnung war fällig am {due_date}",
        })
        risk_score += 15

    # 4. Lieferanten-Risiko
    vendor = invoice_data.get("vendor", "")
    if _is_new_vendor(vendor):
        anomalies.append({
            "type": "Neuer Lieferant",
            "severity": "low",
            "description": f"Lieferant '{vendor}' ist bisher unbekannt",
        })
        risk_score += 10

    risk_score = min(risk_score, 100)

    return {
        "found": len(anomalies) > 0,
        "risk_score": risk_score,
        "details": anomalies,
    }


def _is_duplicate(invoice_data):
    """Prüfe ob Rechnung bereits existiert."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM invoices WHERE vendor = ? AND invoice_number = ?",
            (invoice_data.get("vendor", ""), invoice_data.get("invoice_number", ""))
        )
        count = cur.fetchone()[0]
        conn.close()
        return count > 0
    except Exception:
        return False


def _get_average_amount(vendor):
    """Durchschnittsbetrag des Lieferanten ermitteln."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT AVG(amount) FROM invoices WHERE vendor = ?",
            (vendor,)
        )
        result = cur.fetchone()
        conn.close()
        return result[0] if result and result[0] else None
    except Exception:
        return None


def _is_overdue(due_date):
    """Prüfe ob Fälligkeitsdatum überschritten."""
    from datetime import datetime
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        return due < datetime.now()
    except (ValueError, TypeError):
        return False


def _is_new_vendor(vendor):
    """Prüfe ob Lieferant neu ist."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM invoices WHERE vendor = ?", (vendor,))
        count = cur.fetchone()[0]
        conn.close()
        return count == 0
    except Exception:
        return True
