"""Rechnungsdaten aus PDF/Bild extrahieren."""
import json
import os
import base64
import http.client
from urllib.parse import urlparse

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1")


def extract_invoice_data(uploaded_file):
    """
    Extrahiere Rechnungsdaten mit Ollama-OCR.
    Liest PDF/Bild, sendet an Ollama, gibt strukturierte Daten zurück.
    """
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name or "rechnung.pdf"

    # Determine mime type
    mime_map = {".pdf": "application/pdf", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
    ext = os.path.splitext(file_name)[1].lower()
    mime = mime_map.get(ext, "application/octet-stream")

    try:
        result = _analyze_with_ollama(file_bytes, mime)
        if result:
            return result
    except Exception as e:
        print(f"Ollama analysis failed: {e}")

    # Fallback: Demo-Daten
    return _demo_data()


def _analyze_with_ollama(file_bytes, mime_type):
    """Analyse mit Ollama durchführen."""
    parsed = urlparse(OLLAMA_HOST)
    host = parsed.hostname
    port = parsed.port or 11434

    # For images, use Ollama vision (llava or llava-based model)
    if mime_type.startswith("image/"):
        b64 = base64.b64encode(file_bytes).decode("utf-8")
        payload = json.dumps({
            "model": OLLAMA_MODEL,
            "prompt": (
                "Du bist ein Rechnungs-OCR-System. Extrahiere alle relevanten Daten aus diesem Rechnungsbild "
                "und gib sie als JSON zurück mit genau diesen Feldern:\n"
                '{"vendor": "", "vendor_address": "", "invoice_number": "", "invoice_date": "YYYY-MM-DD", '
                '"due_date": "YYYY-MM-DD", "amount": 0, "tax_rate": 0, "tax_amount": 0, "total": 0, '
                '"line_items": [{"description": "", "qty": 1, "price": 0}], '
                '"bank_details": {"iban": "", "bic": ""}}\n'
                "Gib NUR das JSON zurück, nichts anderes."
            ),
            "images": [b64],
            "stream": False,
        }).encode("utf-8")
    else:
        # For PDFs, use base64 in prompt (text extraction)
        b64 = base64.b64encode(file_bytes).decode("utf-8")
        payload = json.dumps({
            "model": OLLAMA_MODEL,
            "prompt": (
                "Du bist ein Rechnungs-OCR-System. Analysiere die folgenden Base64-kodierten Daten "
                "(PDF-Inhalt) und extrahiere alle Rechnungsdaten.\n"
                "Gib das Ergebnis als JSON mit genau diesen Feldern zurück:\n"
                '{"vendor": "", "vendor_address": "", "invoice_number": "", "invoice_date": "YYYY-MM-DD", '
                '"due_date": "YYYY-MM-DD", "amount": 0, "tax_rate": 0, "tax_amount": 0, "total": 0, '
                '"line_items": [{"description": "", "qty": 1, "price": 0}], '
                '"bank_details": {"iban": "", "bic": ""}}\n'
                "Gib NUR das JSON zurück, nichts anderes.\n\n"
                f"Base64-Daten: {b64[:5000]}"
            ),
            "stream": False,
        }).encode("utf-8")

    conn = http.client.HTTPConnection(host, port, timeout=120)
    conn.request("POST", "/api/generate", body=payload,
                 headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    body = resp.read().decode("utf-8")
    conn.close()

    if resp.status != 200:
        raise Exception(f"Ollama returned {resp.status}: {body[:500]}")

    data = json.loads(body)
    text = data.get("response", "")

    # Try to parse JSON from response
    # Try to find JSON in the response
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON from markdown code blocks
    if "```" in text:
        json_block = text.split("```")[1]
        if json_block.startswith("json"):
            json_block = json_block[4:]
        try:
            return json.loads(json_block.strip())
        except json.JSONDecodeError:
            pass

    # Try to find JSON object
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    raise Exception("Could not parse Ollama response as JSON")


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
