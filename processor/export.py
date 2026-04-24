"""Export-Module für Rechnungsdaten."""
import csv
import io
from datetime import datetime
from database.models import get_connection


def export_invoices(export_format, date_from, date_to):
    """
    Exportiere Rechnungen im gewünschten Format.
    Supported: csv, datev, sap
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT vendor, invoice_number, amount, invoice_date, risk_score, status
        FROM invoices
        WHERE invoice_date BETWEEN ? AND ?
        ORDER BY invoice_date DESC
    """, (str(date_from), str(date_to)))
    rows = cur.fetchall()
    conn.close()

    if export_format == "csv":
        return _export_csv(rows)
    elif export_format == "datev":
        return _export_datev(rows)
    elif export_format == "sap":
        return _export_sap(rows)
    else:
        return _export_csv(rows)


def _export_csv(rows):
    """CSV-Export."""
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow(["Lieferant", "Rechnungsnr.", "Betrag", "Datum", "Risiko", "Status"])
    for row in rows:
        writer.writerow([row[0], row[1], f"{row[2]:.2f}", row[3], row[4], row[5]])
    return output.getvalue().encode("utf-8-sig")


def _export_datev(rows):
    """DATEV-Kompatibler Export (EXTF-Format)."""
    output = io.StringIO()
    output.write("EXTF;510;11000\n")
    output.write("HEADER;11000;100;0\n")
    for row in rows:
        output.write(f"BUCHUNG;11000;0;;{row[1]};{row[0]};;;;{row[2]:.2f};;;;\n")
    output.write("FOOTER;11000;0\n")
    return output.getvalue().encode("utf-8")


def _export_sap(rows):
    """SAP-kompatibler Export."""
    output = io.StringIO()
    output.write("BKPF\tBSEG\t\n")
    for i, row in enumerate(rows):
        output.write(f"\t{i+1}\t{row[0]}\t{row[1]}\t{row[2]:.2f}\t{row[3]}\n")
    return output.getvalue().encode("utf-8")
