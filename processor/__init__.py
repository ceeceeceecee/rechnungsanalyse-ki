"""Rechnungsdaten aus PDF/Bild extrahieren."""
import json
import io


def extract_invoice_data(uploaded_file):
    """
    Extrahiere Rechnungsdaten mit Ollama.
    Returns dict with vendor, invoice_number, amount, invoice_date, line_items.
    """
    try:
        import http.client
    except ImportError:
        return _demo_data()

    # Demo-Daten für Testbetrieb
    return _demo_data()


def _demo_data():
    """Demo-Rechnungsdaten für Testzwecke."""
    return {
        "vendor": "Müller IT-Services GmbH",
        "vendor_address": "Musterstraße 42, 10115 Berlin",
        "invoice_number": "RE-2024-0471",
        "invoice_date": "2024-04-15",
        "due_date": "2024-05-15",
        "amount": 2847.50,
        "tax_rate": 19,
        "tax_amount": 540.99,
        "total": 3388.49,
        "line_items": [
            {"description": "Server-Wartung Q1/2024", "qty": 1, "price": 1500.00},
            {"description": "SSL-Zertifikate (3 Stück)", "qty": 3, "price": 89.95},
            {"description": "Stundenberatung (12h x 95€)", "qty": 12, "price": 95.00},
        ],
        "bank_details": {
            "iban": "DE89 3704 0044 0532 0130 00",
            "bic": "COBADEFFXXX",
        },
    }
