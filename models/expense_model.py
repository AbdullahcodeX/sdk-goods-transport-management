"""
SDK GOODS - Goods Transport Management System
Expense Model
--------------------------------
Handles all Fixed and Other expenses linked to a specific trip
(Tools, Food, Tyre, Police, Inaam, Motorway Toll, GT Road Toll, etc.)
"""

from database.db_mana


def add_expense(trip_id, expense_group, category, amount, description, expense_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO expenses (trip_id, expense_group, category, amount, description, expense_date)
        VALUES (?,?,?,?,?,?)
    """, (trip_id, expense_group, category, float(amount), description, expense_date))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_expenses_by_trip(trip_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM expenses WHERE trip_id = ? ORDER BY expense_date, id",
        (trip_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_expense(expense_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


def get_total_expenses_by_trip(trip_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM expenses WHERE trip_id = ?",
        (trip_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row["total"] if row else 0.0
