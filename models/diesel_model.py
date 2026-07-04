"""
SDK GOODS - Goods Transport Management System
Diesel Model
--------------------------------
Handles diesel purchase entries per trip (Irani / Pakistani / Other).
"""

from database.db_manager import get_connection


def add_diesel(trip_id, diesel_type, liters, rate_per_liter, total_cost, pump_location, diesel_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO diesel (trip_id, diesel_type, liters, rate_per_liter, total_cost, pump_location, diesel_date)
        VALUES (?,?,?,?,?,?,?)
    """, (trip_id, diesel_type, float(liters), float(rate_per_liter), float(total_cost), pump_location, diesel_date))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_diesel_by_trip(trip_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM diesel WHERE trip_id = ? ORDER BY diesel_date, id",
        (trip_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_diesel(diesel_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM diesel WHERE id = ?", (diesel_id,))
    conn.commit()
    conn.close()


def get_total_diesel_by_trip(trip_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COALESCE(SUM(total_cost), 0) AS total FROM diesel WHERE trip_id = ?",
        (trip_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row["total"] if row else 0.0
