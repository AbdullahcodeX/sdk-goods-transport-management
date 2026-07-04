"""
SDK GOODS - Goods Transport Management System
Database Manager
--------------------------------
Handles the SQLite connection and creation of all tables.
This file is the single source of truth for the database schema.
"""

import sqlite3
import os

# The database file will live in a fixed folder so it works the same
# whether run as a .py script or as a packaged .exe.
APP_FOLDER_NAME = "SDK_GOODS_TransportApp"


def get_db_path():
    """
    Returns a safe, writable path for the database file.
    On the client's PC this will be: Documents/SDK_GOODS_TransportApp/transport.db
    This ensures the .exe always has write permission (unlike Program Files).
    """
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    app_folder = os.path.join(documents_path, APP_FOLDER_NAME)
    os.makedirs(app_folder, exist_ok=True)
    return os.path.join(app_folder, "transport.db")


def get_connection():
    """Returns a new SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect(get_db_path())
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row  # allows dict-like access to rows
    return conn


def initialize_database():
    """
    Creates all required tables if they do not already exist.
    Safe to call every time the app starts.
    """
    conn = get_connection()
    cur = conn.cursor()

    # 1. VEHICLES TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_number TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active',
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    """)

    # 2. TRIPS TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            receipt_no TEXT UNIQUE,
            trip_date TEXT NOT NULL,
            from_city TEXT NOT NULL,
            to_city TEXT NOT NULL,
            goods_details TEXT,
            weight REAL DEFAULT 0,
            weight_unit TEXT DEFAULT 'Tons',
            broker_name TEXT,
            broker_contact TEXT,
            station_details TEXT,
            total_brokery REAL DEFAULT 0,
            wasool_kiraya REAL DEFAULT 0,
            remaining_kiraya REAL DEFAULT 0,
            daily_wages REAL DEFAULT 0,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        )
    """)

    # 3. EXPENSES TABLE (Fixed + Other, per trip)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            expense_group TEXT NOT NULL,      -- 'Fixed' or 'Other'
            category TEXT NOT NULL,           -- Toll, Food, Tyre, Police, Inaam, Motorway Toll, GT Road Toll, Other...
            amount REAL NOT NULL DEFAULT 0,
            description TEXT,
            expense_date TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
        )
    """)

    # 4. DIESEL TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS diesel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            diesel_type TEXT NOT NULL,        -- Irani, Pakistani, Other
            liters REAL DEFAULT 0,
            rate_per_liter REAL DEFAULT 0,
            total_cost REAL DEFAULT 0,
            pump_location TEXT,
            diesel_date TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
        )
    """)

    # 5. SETTINGS TABLE (single row - company info)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            company_name TEXT DEFAULT 'SDK GOODS',
            owner_name TEXT,
            address TEXT,
            phone TEXT,
            logo_path TEXT
        )
    """)

    # Insert default settings row (only once) with your company name pre-filled
    cur.execute("""
        INSERT OR IGNORE INTO settings (id, company_name)
        VALUES (1, 'SDK GOODS')
    """)

    conn.commit()
    conn.close()
    print(f"[SDK GOODS] Database ready at: {get_db_path()}")


if __name__ == "__main__":
    # Running this file directly will create/verify the database.
    initialize_database()
