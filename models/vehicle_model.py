"""
SDK GOODS - Goods Transport Management System
Vehicle Model
--------------------------------
All database read/write logic for vehicles lives here.
The UI (vehicle_screen.py) never talks to SQLite directly —
it always goes through these functions.
"""

from database.db_manager import get_connection


def add_vehicle(vehicle_number, city, status="Active"):
    """Adds a new vehicle. Raises ValueError if the vehicle number already exists."""
    vehicle_number = vehicle_number.strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vehicles WHERE vehicle_number = ?", (vehicle_number,))
    if cur.fetchone():
        conn.close()
        raise ValueError(f"Vehicle number '{vehicle_number}' already exists.")

    cur.execute(
        "INSERT INTO vehicles (vehicle_number, city, status) VALUES (?, ?, ?)",
        (vehicle_number, city, status),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_all_vehicles(search_text=None):
    """Returns all vehicles, optionally filtered by vehicle number or city."""
    conn = get_connection()
    cur = conn.cursor()
    if search_text:
        like = f"%{search_text}%"
        cur.execute(
            "SELECT * FROM vehicles WHERE vehicle_number LIKE ? OR city LIKE ? ORDER BY id DESC",
            (like, like),
        )
    else:
        cur.execute("SELECT * FROM vehicles ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_vehicle(vehicle_id):
    """Returns a single vehicle row by id, or None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
    row = cur.fetchone()
    conn.close()
    return row


def update_vehicle(vehicle_id, vehicle_number, city, status):
    """Updates an existing vehicle. Raises ValueError on duplicate vehicle number."""
    vehicle_number = vehicle_number.strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM vehicles WHERE vehicle_number = ? AND id != ?",
        (vehicle_number, vehicle_id),
    )
    if cur.fetchone():
        conn.close()
        raise ValueError(f"Vehicle number '{vehicle_number}' already exists.")

    cur.execute(
        "UPDATE vehicles SET vehicle_number = ?, city = ?, status = ? WHERE id = ?",
        (vehicle_number, city, status, vehicle_id),
    )
    conn.commit()
    conn.close()


def set_vehicle_status(vehicle_id, status):
    """Quickly toggles a vehicle's status (Active / Inactive / In Workshop)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE vehicles SET status = ? WHERE id = ?", (status, vehicle_id))
    conn.commit()
    conn.close()


def count_vehicles():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS total FROM vehicles")
    row = cur.fetchone()
    conn.close()
    return row["total"] if row else 0
