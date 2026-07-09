"""
SDK GOODS - Goods Transport Management System
Trip Model
--------------------------------
All database logic for trips. Remaining Kiraya is always
auto-calculated as (Total Brokery - Wasool Kiraya) whenever a
trip is added or updated, so the numbers can never go out of sync.
"""

from database.db_manager import get_connecti


def _safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def add_trip(vehicle_id, trip_date, from_city, to_city, goods_details,
             weight, weight_unit, broker_name, broker_contact, station_details,
             total_brokery, wasool_kiraya, daily_wages, notes):
    total_brokery = _safe_float(total_brokery)
    wasool_kiraya = _safe_float(wasool_kiraya)
    remaining_kiraya = total_brokery - wasool_kiraya

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO trips (
            vehicle_id, trip_date, from_city, to_city, goods_details,
            weight, weight_unit, broker_name, broker_contact, station_details,
            total_brokery, wasool_kiraya, remaining_kiraya, daily_wages, notes
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        vehicle_id, trip_date, from_city, to_city, goods_details,
        _safe_float(weight), weight_unit, broker_name, broker_contact, station_details,
        total_brokery, wasool_kiraya, remaining_kiraya, _safe_float(daily_wages), notes
    ))
    trip_id = cur.lastrowid

    # Auto-generate a professional receipt number now that we have the ID
    receipt_no = f"TRIP-{trip_id:06d}"
    cur.execute("UPDATE trips SET receipt_no = ? WHERE id = ?", (receipt_no, trip_id))

    conn.commit()
    conn.close()
    return trip_id


def update_trip(trip_id, trip_date, from_city, to_city, goods_details,
                weight, weight_unit, broker_name, broker_contact, station_details,
                total_brokery, wasool_kiraya, daily_wages, notes):
    total_brokery = _safe_float(total_brokery)
    wasool_kiraya = _safe_float(wasool_kiraya)
    remaining_kiraya = total_brokery - wasool_kiraya

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE trips SET
            trip_date=?, from_city=?, to_city=?, goods_details=?,
            weight=?, weight_unit=?, broker_name=?, broker_contact=?, station_details=?,
            total_brokery=?, wasool_kiraya=?, remaining_kiraya=?, daily_wages=?, notes=?
        WHERE id=?
    """, (
        trip_date, from_city, to_city, goods_details,
        _safe_float(weight), weight_unit, broker_name, broker_contact, station_details,
        total_brokery, wasool_kiraya, remaining_kiraya, _safe_float(daily_wages), notes,
        trip_id
    ))
    conn.commit()
    conn.close()


def get_trips_by_vehicle(vehicle_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM trips WHERE vehicle_id = ? ORDER BY trip_date DESC, id DESC",
        (vehicle_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_trip(trip_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM trips WHERE id = ?", (trip_id,))
    row = cur.fetchone()
    conn.close()
    return row


def get_all_trips():
    """All trips across all vehicles, joined with the vehicle number - used in dashboard/reports."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT trips.*, vehicles.vehicle_number AS vehicle_number
        FROM trips
        JOIN vehicles ON trips.vehicle_id = vehicles.id
        ORDER BY trips.trip_date DESC, trips.id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_trips_by_vehicle_and_month(vehicle_id, year_month):
    """year_month must be in 'YYYY-MM' format, e.g. '2026-07'."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM trips
        WHERE vehicle_id = ? AND strftime('%Y-%m', trip_date) = ?
        ORDER BY trip_date
    """, (vehicle_id, year_month))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_distinct_months_for_vehicle(vehicle_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT strftime('%Y-%m', trip_date) AS ym
        FROM trips WHERE vehicle_id = ?
        ORDER BY ym DESC
    """, (vehicle_id,))
    rows = [r["ym"] for r in cur.fetchall() if r["ym"]]
    conn.close()
    return rows


def delete_trip(trip_id):
    """Deletes a trip. Its expenses and diesel entries are removed automatically (cascade)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM trips WHERE id = ?", (trip_id,))
    conn.commit()
    conn.close()


def count_trips():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS total FROM trips")
    row = cur.fetchone()
    conn.close()
    return row["total"] if row else 0
