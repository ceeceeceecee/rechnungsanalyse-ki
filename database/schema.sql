"""SQLite Schema für Rechnungsanalyse-KI."""

SCHEMA = """
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor TEXT NOT NULL,
    invoice_number TEXT,
    amount REAL NOT NULL DEFAULT 0,
    invoice_date TEXT,
    due_date TEXT,
    risk_score INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'ok',
    raw_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    iban TEXT,
    bic TEXT,
    total_invoices INTEGER DEFAULT 0,
    total_amount REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS export_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    export_format TEXT NOT NULL,
    record_count INTEGER,
    exported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_invoices_vendor ON invoices(vendor);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_invoices_risk ON invoices(risk_score);
"""
