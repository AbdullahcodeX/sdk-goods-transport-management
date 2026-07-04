"""
SDK GOODS - Goods Transport Management System
Settings Model
--------------------------------
Stores and retrieves the single-row company settings
(company name, owner, address, phone).
"""

from database.db_manager import get_connection


def get_settings():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM settings WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    return row


def update_settings(company_name, owner_name, address, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE settings SET company_name=?, owner_name=?, address=?, phone=?
        WHERE id = 1
    """, (company_name, owner_name, address, phone))
    conn.commit()
    conn.close()
