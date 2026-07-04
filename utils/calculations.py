"""
SDK GOODS - Goods Transport Management System
Calculations
--------------------------------
Central place for every "money math" formula in the app, so the
Ledger, Dashboard, and Monthly Report screens always agree with
each other.

Formulas:
    Total Expense (per trip) = Sum(expenses) + Sum(diesel) + Daily Wages
    Net Saving (per trip)    = Wasool Kiraya - Total Expense
    Remaining Kiraya         = Total Brokery - Wasool Kiraya   (done in trip_model.py)
"""

from models.expense_model import get_total_expenses_by_trip
from models.diesel_model import get_total_diesel_by_trip
from models.trip_model import get_trips_by_vehicle, get_trips_by_vehicle_and_month, get_all_trips
from models.vehicle_model import get_all_vehicles


def compute_trip_totals(trip):
    """trip must be a sqlite3.Row (or dict) with at least 'id', 'wasool_kiraya', 'daily_wages'."""
    total_expenses = get_total_expenses_by_trip(trip["id"])
    total_diesel = get_total_diesel_by_trip(trip["id"])
    daily_wages = trip["daily_wages"] or 0
    total_cost = total_expenses + total_diesel + daily_wages
    wasool_kiraya = trip["wasool_kiraya"] or 0
    net_saving = wasool_kiraya - total_cost

    return {
        "total_expenses": total_expenses,
        "total_diesel": total_diesel,
        "daily_wages": daily_wages,
        "total_cost": total_cost,
        "wasool_kiraya": wasool_kiraya,
        "net_saving": net_saving,
    }


def compute_vehicle_summary(vehicle_id):
    """Aggregates every trip ever made by one vehicle."""
    trips = get_trips_by_vehicle(vehicle_id)
    summary = {
        "trip_count": len(trips), "total_wasool": 0.0, "total_expenses": 0.0,
        "total_diesel": 0.0, "total_wages": 0.0, "total_cost": 0.0, "net_saving": 0.0,
    }
    for t in trips:
        totals = compute_trip_totals(t)
        summary["total_wasool"] += totals["wasool_kiraya"]
        summary["total_expenses"] += totals["total_expenses"]
        summary["total_diesel"] += totals["total_diesel"]
        summary["total_wages"] += totals["daily_wages"]
        summary["total_cost"] += totals["total_cost"]
        summary["net_saving"] += totals["net_saving"]
    return summary


def compute_vehicle_month_summary(vehicle_id, year_month):
    """Aggregates only the trips of one vehicle within a given 'YYYY-MM' month."""
    trips = get_trips_by_vehicle_and_month(vehicle_id, year_month)
    summary = {
        "trip_count": len(trips), "total_wasool": 0.0, "total_expenses": 0.0,
        "total_diesel": 0.0, "total_wages": 0.0, "total_cost": 0.0, "net_saving": 0.0,
    }
    for t in trips:
        totals = compute_trip_totals(t)
        summary["total_wasool"] += totals["wasool_kiraya"]
        summary["total_expenses"] += totals["total_expenses"]
        summary["total_diesel"] += totals["total_diesel"]
        summary["total_wages"] += totals["daily_wages"]
        summary["total_cost"] += totals["total_cost"]
        summary["net_saving"] += totals["net_saving"]
    return summary, trips


def compute_global_summary():
    """Company-wide totals across every vehicle and every trip."""
    vehicles = get_all_vehicles()
    trips = get_all_trips()
    summary = {
        "total_vehicles": len(vehicles), "total_trips": len(trips),
        "total_wasool": 0.0, "total_expenses": 0.0, "total_diesel": 0.0,
        "total_wages": 0.0, "total_cost": 0.0, "net_saving": 0.0,
    }
    for t in trips:
        totals = compute_trip_totals(t)
        summary["total_wasool"] += totals["wasool_kiraya"]
        summary["total_expenses"] += totals["total_expenses"]
        summary["total_diesel"] += totals["total_diesel"]
        summary["total_wages"] += totals["daily_wages"]
        summary["total_cost"] += totals["total_cost"]
        summary["net_saving"] += totals["net_saving"]
    return summary
