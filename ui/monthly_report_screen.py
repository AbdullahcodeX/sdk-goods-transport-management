"""
SDK GOODS - Goods Transport Management System
Monthly Report Screen
--------------------------------
Pick a vehicle + a month that has recorded trips, and see the
aggregated income, expense, diesel, wages, and net saving for
that month, plus the list of trips within it.
"""

import tkinter as tk
from tkinter import ttk

from models.vehicle_model import get_all_vehicles
from models.trip_model import get_distinct_months_for_vehicle
from utils.calculations import compute_vehicle_month_summary, compute_trip_totals
from ui.widgets.styled_widgets import (
    COLOR_CONTENT_BG, COLOR_CARD_BG, COLOR_TEXT_DARK, COLOR_HEADER_BG,
    COLOR_DANGER, COLOR_SUCCESS, FONT_HEADER, FONT_LABEL, FONT_LABEL_BOLD, FONT_CARD_VALUE,
)


class MonthlyReportScreen(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_CONTENT_BG, **kwargs)
        self.vehicles = get_all_vehicles()

        if not self.vehicles:
            tk.Label(
                self, text="No vehicles found. Please add a vehicle first.",
                bg=COLOR_CONTENT_BG, fg=COLOR_DANGER, font=FONT_HEADER
            ).pack(pady=40)
            return

        self._build_selectors()
        self._build_summary_cards()
        self._build_table()
        self.on_vehicle_change()

    # ---------------------------------------------------------
    def _build_selectors(self):
        frame = tk.Frame(self, bg=COLOR_CONTENT_BG)
        frame.pack(fill="x", padx=25, pady=(20, 5))

        tk.Label(frame, text="Vehicle:", bg=COLOR_CONTENT_BG, font=FONT_LABEL_BOLD).pack(side="left", padx=(0, 8))
        self.vehicle_labels = [f'{v["vehicle_number"]} ({v["city"]})' for v in self.vehicles]
        self.vehicle_var = tk.StringVar()
        self.vehicle_combo = ttk.Combobox(
            frame, textvariable=self.vehicle_var, values=self.vehicle_labels, state="readonly", width=28
        )
        self.vehicle_combo.pack(side="left", padx=(0, 20))
        self.vehicle_combo.current(0)
        self.vehicle_combo.bind("<<ComboboxSelected>>", lambda e: self.on_vehicle_change())

        tk.Label(frame, text="Month:", bg=COLOR_CONTENT_BG, font=FONT_LABEL_BOLD).pack(side="left", padx=(0, 8))
        self.month_var = tk.StringVar()
        self.month_combo = ttk.Combobox(frame, textvariable=self.month_var, values=[], state="readonly", width=15)
        self.month_combo.pack(side="left")
        self.month_combo.bind("<<ComboboxSelected>>", lambda e: self.generate_report())

    def on_vehicle_change(self):
        idx = self.vehicle_combo.current()
        if idx < 0 or idx >= len(self.vehicles):
            return
        vehicle = self.vehicles[idx]
        months = get_distinct_months_for_vehicle(vehicle["id"])
        self.month_combo.configure(values=months)
        if months:
            self.month_combo.current(0)
        else:
            self.month_var.set("")
        self.generate_report()

    def get_selected_vehicle(self):
        idx = self.vehicle_combo.current()
        if idx < 0 or idx >= len(self.vehicles):
            return None
        return self.vehicles[idx]

    # ---------------------------------------------------------
    def _build_summary_cards(self):
        self.cards_frame = tk.Frame(self, bg=COLOR_CONTENT_BG)
        self.cards_frame.pack(fill="x", padx=25, pady=(15, 10))
        self.card_labels = {}

        card_defs = [
            ("trip_count", "Trips This Month", COLOR_TEXT_DARK),
            ("total_wasool", "Total Income (Wasool)", COLOR_SUCCESS),
            ("total_cost", "Total Expense", COLOR_DANGER),
            ("net_saving", "Net Saving", COLOR_SUCCESS),
        ]
        for key, label, color in card_defs:
            card = tk.Frame(self.cards_frame, bg=COLOR_CARD_BG, padx=15, pady=12)
            card.pack(side="left", fill="both", expand=True, padx=6)
            tk.Label(card, text=label, bg=COLOR_CARD_BG, fg="#6B7280", font=FONT_LABEL).pack(anchor="w")
            value_label = tk.Label(card, text="0", bg=COLOR_CARD_BG, fg=color, font=FONT_CARD_VALUE)
            value_label.pack(anchor="w", pady=(4, 0))
            self.card_labels[key] = value_label

    # ---------------------------------------------------------
    def _build_table(self):
        card = tk.Frame(self, bg=COLOR_CARD_BG)
        card.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        self.table_title = tk.Label(
            card, text="Trips in Selected Month", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        )
        self.table_title.pack(anchor="w", padx=20, pady=(15, 10))

        columns = ("receipt_no", "date", "route", "wasool", "expense", "saving")
        headings = {
            "receipt_no": "Receipt #", "date": "Date", "route": "Route",
            "wasool": "Wasool Kiraya", "expense": "Total Expense", "saving": "Net Saving"
        }
        widths = {"receipt_no": 100, "date": 100, "route": 200, "wasool": 110, "expense": 110, "saving": 110}

        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w" if col == "route" else "center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.tree.tag_configure("positive", foreground=COLOR_SUCCESS)
        self.tree.tag_configure("negative", foreground=COLOR_DANGER)

    # ---------------------------------------------------------
    def generate_report(self):
        vehicle = self.get_selected_vehicle()
        year_month = self.month_var.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        if not vehicle or not year_month:
            for key in self.card_labels:
                self.card_labels[key].configure(text="0")
            self.table_title.configure(text="No trips recorded yet for this vehicle")
            return

        summary, trips = compute_vehicle_month_summary(vehicle["id"], year_month)

        self.card_labels["trip_count"].configure(text=str(summary["trip_count"]))
        self.card_labels["total_wasool"].configure(text=f'Rs {summary["total_wasool"]:,.0f}')
        self.card_labels["total_cost"].configure(text=f'Rs {summary["total_cost"]:,.0f}')
        net = summary["net_saving"]
        net_color = COLOR_SUCCESS if net >= 0 else COLOR_DANGER
        self.card_labels["net_saving"].configure(text=f'Rs {net:,.0f}', fg=net_color)

        self.table_title.configure(text=f'Trips in {year_month} — {vehicle["vehicle_number"]}')

        for t in trips:
            totals = compute_trip_totals(t)
            tag = "positive" if totals["net_saving"] >= 0 else "negative"
            route = f'{t["from_city"]} -> {t["to_city"]}'
            self.tree.insert("", "end", values=(
                t["receipt_no"], t["trip_date"], route,
                f'{totals["wasool_kiraya"]:,.0f}', f'{totals["total_cost"]:,.0f}', f'{totals["net_saving"]:,.0f}'
            ), tags=(tag,))
