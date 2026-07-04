"""
SDK GOODS - Goods Transport Management System
Dashboard Screen
--------------------------------
Company-wide summary cards (all vehicles combined) + a per-vehicle
table of totals/savings. Double-click a vehicle row to see its
trip-by-trip breakdown below.
"""

import tkinter as tk
from tkinter import ttk

from models.vehicle_model import get_all_vehicles
from models.trip_model import get_trips_by_vehicle
from utils.calculations import compute_global_summary, compute_vehicle_summary, compute_trip_totals
from ui.widgets.styled_widgets import (
    COLOR_CONTENT_BG, COLOR_CARD_BG, COLOR_TEXT_DARK, COLOR_HEADER_BG,
    COLOR_DANGER, COLOR_SUCCESS, FONT_HEADER, FONT_LABEL, FONT_LABEL_BOLD, FONT_CARD_VALUE,
)


class DashboardScreen(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_CONTENT_BG, **kwargs)
        self.vehicles = get_all_vehicles()

        self._build_summary_cards()
        self._build_vehicle_table()
        self._build_trip_detail_table()
        self.refresh_all()

    # ---------------------------------------------------------
    def _build_summary_cards(self):
        self.cards_frame = tk.Frame(self, bg=COLOR_CONTENT_BG)
        self.cards_frame.pack(fill="x", padx=25, pady=(20, 10))
        self.card_labels = {}

        card_defs = [
            ("total_vehicles", "Total Vehicles", COLOR_TEXT_DARK),
            ("total_trips", "Total Trips", COLOR_TEXT_DARK),
            ("total_wasool", "Total Income (Wasool)", COLOR_SUCCESS),
            ("total_cost", "Total Expense (All)", COLOR_DANGER),
            ("net_saving", "Net Saving (Company)", COLOR_SUCCESS),
        ]
        for key, label, color in card_defs:
            card = tk.Frame(self.cards_frame, bg=COLOR_CARD_BG, padx=15, pady=12)
            card.pack(side="left", fill="both", expand=True, padx=6)
            tk.Label(card, text=label, bg=COLOR_CARD_BG, fg="#6B7280", font=FONT_LABEL).pack(anchor="w")
            value_label = tk.Label(card, text="0", bg=COLOR_CARD_BG, fg=color, font=FONT_CARD_VALUE)
            value_label.pack(anchor="w", pady=(4, 0))
            self.card_labels[key] = value_label

    def refresh_summary_cards(self):
        summary = compute_global_summary()
        self.card_labels["total_vehicles"].configure(text=str(summary["total_vehicles"]))
        self.card_labels["total_trips"].configure(text=str(summary["total_trips"]))
        self.card_labels["total_wasool"].configure(text=f'Rs {summary["total_wasool"]:,.0f}')
        self.card_labels["total_cost"].configure(text=f'Rs {summary["total_cost"]:,.0f}')

        net = summary["net_saving"]
        net_color = COLOR_SUCCESS if net >= 0 else COLOR_DANGER
        self.card_labels["net_saving"].configure(text=f'Rs {net:,.0f}', fg=net_color)

    # ---------------------------------------------------------
    def _build_vehicle_table(self):
        card = tk.Frame(self, bg=COLOR_CARD_BG)
        card.pack(fill="both", expand=True, padx=25, pady=(10, 10))

        tk.Label(
            card, text="Per-Vehicle Summary (double-click a row to see its trips)",
            font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=20, pady=(15, 10))

        columns = ("id", "vehicle_number", "city", "status", "trips", "wasool", "expense", "saving")
        headings = {
            "id": "ID", "vehicle_number": "Vehicle Number", "city": "City", "status": "Status",
            "trips": "Trips", "wasool": "Total Wasool", "expense": "Total Expense", "saving": "Net Saving"
        }
        widths = {
            "id": 40, "vehicle_number": 150, "city": 130, "status": 100,
            "trips": 60, "wasool": 110, "expense": 110, "saving": 110
        }

        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w" if col in ("vehicle_number", "city") else "center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.tree.tag_configure("positive", foreground=COLOR_SUCCESS)
        self.tree.tag_configure("negative", foreground=COLOR_DANGER)

        self.tree.bind("<Double-1>", self.on_vehicle_double_click)

    def refresh_vehicle_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for v in self.vehicles:
            summary = compute_vehicle_summary(v["id"])
            tag = "positive" if summary["net_saving"] >= 0 else "negative"
            self.tree.insert("", "end", values=(
                v["id"], v["vehicle_number"], v["city"], v["status"],
                summary["trip_count"], f'{summary["total_wasool"]:,.0f}',
                f'{summary["total_cost"]:,.0f}', f'{summary["net_saving"]:,.0f}'
            ), tags=(tag,))

    def on_vehicle_double_click(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0])["values"]
        vehicle_id = values[0]
        vehicle_number = values[1]
        self.load_vehicle_trips(vehicle_id, vehicle_number)

    # ---------------------------------------------------------
    def _build_trip_detail_table(self):
        card = tk.Frame(self, bg=COLOR_CARD_BG)
        card.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        self.detail_title = tk.Label(
            card, text="Select a vehicle above to see its trip-by-trip breakdown",
            font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        )
        self.detail_title.pack(anchor="w", padx=20, pady=(15, 10))

        columns = ("receipt_no", "date", "route", "wasool", "expense", "saving")
        headings = {
            "receipt_no": "Receipt #", "date": "Date", "route": "Route",
            "wasool": "Wasool Kiraya", "expense": "Total Expense", "saving": "Net Saving"
        }
        widths = {"receipt_no": 100, "date": 100, "route": 200, "wasool": 110, "expense": 110, "saving": 110}

        self.detail_tree = ttk.Treeview(card, columns=columns, show="headings", height=8)
        for col in columns:
            self.detail_tree.heading(col, text=headings[col])
            self.detail_tree.column(col, width=widths[col], anchor="w" if col == "route" else "center")
        self.detail_tree.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.detail_tree.tag_configure("positive", foreground=COLOR_SUCCESS)
        self.detail_tree.tag_configure("negative", foreground=COLOR_DANGER)

    def load_vehicle_trips(self, vehicle_id, vehicle_number):
        self.detail_title.configure(text=f"Trip-by-Trip Breakdown — {vehicle_number}")
        for row in self.detail_tree.get_children():
            self.detail_tree.delete(row)

        trips = get_trips_by_vehicle(vehicle_id)
        for t in trips:
            totals = compute_trip_totals(t)
            tag = "positive" if totals["net_saving"] >= 0 else "negative"
            route = f'{t["from_city"]} -> {t["to_city"]}'
            self.detail_tree.insert("", "end", values=(
                t["receipt_no"], t["trip_date"], route,
                f'{totals["wasool_kiraya"]:,.0f}', f'{totals["total_cost"]:,.0f}', f'{totals["net_saving"]:,.0f}'
            ), tags=(tag,))

    # ---------------------------------------------------------
    def refresh_all(self):
        self.vehicles = get_all_vehicles()
        self.refresh_summary_cards()
        self.refresh_vehicle_table()
