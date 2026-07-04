"""
SDK GOODS - Goods Transport Management System
Ledger Book Screen
--------------------------------
Read-only, full itemized "statement" for one trip:
trip info + all expenses + all diesel entries + final totals
(Total Expense, Net Saving). This is the professional ledger
book view of a single trip.
"""

import tkinter as tk
from tkinter import ttk

from models.vehicle_model import get_all_vehicles
from models.trip_model import get_trips_by_vehicle
from models.expense_model import get_expenses_by_trip
from models.diesel_model import get_diesel_by_trip
from utils.calculations import compute_trip_totals
from ui.widgets.styled_widgets import (
    COLOR_CONTENT_BG, COLOR_CARD_BG, COLOR_TEXT_DARK, COLOR_HEADER_BG,
    COLOR_DANGER, COLOR_SUCCESS, FONT_HEADER, FONT_LABEL, FONT_LABEL_BOLD, FONT_CARD_VALUE,
)


class LedgerScreen(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_CONTENT_BG, **kwargs)
        self.vehicles = get_all_vehicles()
        self.trips = []

        if not self.vehicles:
            tk.Label(
                self, text="No vehicles found. Please add a vehicle first.",
                bg=COLOR_CONTENT_BG, fg=COLOR_DANGER, font=FONT_HEADER
            ).pack(pady=40)
            return

        self._build_selectors()
        self._build_ledger_area()
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

        tk.Label(frame, text="Trip:", bg=COLOR_CONTENT_BG, font=FONT_LABEL_BOLD).pack(side="left", padx=(0, 8))
        self.trip_var = tk.StringVar()
        self.trip_combo = ttk.Combobox(frame, textvariable=self.trip_var, values=[], state="readonly", width=45)
        self.trip_combo.pack(side="left")
        self.trip_combo.bind("<<ComboboxSelected>>", lambda e: self.render_ledger())

    def on_vehicle_change(self):
        idx = self.vehicle_combo.current()
        if idx < 0 or idx >= len(self.vehicles):
            return
        vehicle = self.vehicles[idx]
        self.trips = get_trips_by_vehicle(vehicle["id"])
        trip_labels = [f'{t["receipt_no"]} | {t["trip_date"]} | {t["from_city"]}->{t["to_city"]}' for t in self.trips]
        self.trip_combo.configure(values=trip_labels)
        if trip_labels:
            self.trip_combo.current(0)
        else:
            self.trip_var.set("")
        self.render_ledger()

    def get_selected_trip(self):
        idx = self.trip_combo.current()
        if idx < 0 or idx >= len(self.trips):
            return None
        return self.trips[idx]

    # ---------------------------------------------------------
    def _build_ledger_area(self):
        # Scrollable container so long ledgers don't get cut off
        outer = tk.Frame(self, bg=COLOR_CONTENT_BG)
        outer.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        canvas = tk.Canvas(outer, bg=COLOR_CONTENT_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        self.ledger_frame = tk.Frame(canvas, bg=COLOR_CONTENT_BG)

        self.ledger_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.ledger_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _clear_ledger(self):
        for widget in self.ledger_frame.winfo_children():
            widget.destroy()

    def render_ledger(self):
        self._clear_ledger()
        trip = self.get_selected_trip()
        if not trip:
            tk.Label(
                self.ledger_frame, text="No trip selected.", bg=COLOR_CONTENT_BG, font=FONT_LABEL
            ).pack(pady=20)
            return

        # ---- Trip Info Card ----
        info_card = tk.Frame(self.ledger_frame, bg=COLOR_CARD_BG)
        info_card.pack(fill="x", pady=(0, 15))

        tk.Label(
            info_card, text=f"Trip Ledger - {trip['receipt_no']}", font=FONT_HEADER,
            bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=20, pady=(15, 10))

        info_pairs = [
            ("Date", trip["trip_date"]),
            ("Route", f'{trip["from_city"]} -> {trip["to_city"]}'),
            ("Goods / Maal", trip["goods_details"] or "-"),
            ("Weight", f'{trip["weight"]} {trip["weight_unit"]}'),
            ("Broker", f'{trip["broker_name"] or "-"} ({trip["broker_contact"] or "-"})'),
            ("Station", trip["station_details"] or "-"),
            ("Notes", trip["notes"] or "-"),
        ]
        info_grid = tk.Frame(info_card, bg=COLOR_CARD_BG)
        info_grid.pack(fill="x", padx=20, pady=(0, 15))
        for i, (label, value) in enumerate(info_pairs):
            tk.Label(info_grid, text=f"{label}:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
                .grid(row=i, column=0, sticky="w", pady=2)
            tk.Label(info_grid, text=value, font=FONT_LABEL, bg=COLOR_CARD_BG)\
                .grid(row=i, column=1, sticky="w", padx=(10, 0), pady=2)

        # ---- Expenses Table ----
        exp_card = tk.Frame(self.ledger_frame, bg=COLOR_CARD_BG)
        exp_card.pack(fill="x", pady=(0, 15))
        tk.Label(
            exp_card, text="Expenses", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=20, pady=(15, 10))

        expenses = get_expenses_by_trip(trip["id"])
        exp_columns = ("group", "category", "amount", "description", "date")
        exp_tree = ttk.Treeview(exp_card, columns=exp_columns, show="headings", height=min(6, max(2, len(expenses))))
        exp_headings = {"group": "Group", "category": "Category", "amount": "Amount", "description": "Description", "date": "Date"}
        exp_widths = {"group": 70, "category": 190, "amount": 100, "description": 220, "date": 100}
        for col in exp_columns:
            exp_tree.heading(col, text=exp_headings[col])
            exp_tree.column(col, width=exp_widths[col], anchor="w" if col in ("category", "description") else "center")
        for e in expenses:
            exp_tree.insert("", "end", values=(e["expense_group"], e["category"], f'{e["amount"]:,.0f}', e["description"] or "", e["expense_date"]))
        exp_tree.pack(fill="x", padx=20, pady=(0, 15))
        if not expenses:
            tk.Label(exp_card, text="No expenses recorded for this trip.", bg=COLOR_CARD_BG, fg="#6B7280", font=FONT_LABEL).pack(anchor="w", padx=20, pady=(0, 10))

        # ---- Diesel Table ----
        diesel_card = tk.Frame(self.ledger_frame, bg=COLOR_CARD_BG)
        diesel_card.pack(fill="x", pady=(0, 15))
        tk.Label(
            diesel_card, text="Diesel Entries", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=20, pady=(15, 10))

        diesel_entries = get_diesel_by_trip(trip["id"])
        d_columns = ("type", "liters", "rate", "total", "pump", "date")
        d_tree = ttk.Treeview(diesel_card, columns=d_columns, show="headings", height=min(6, max(2, len(diesel_entries))))
        d_headings = {"type": "Type", "liters": "Liters", "rate": "Rate/Liter", "total": "Total Cost", "pump": "Pump/Location", "date": "Date"}
        d_widths = {"type": 130, "liters": 70, "rate": 90, "total": 100, "pump": 180, "date": 100}
        for col in d_columns:
            d_tree.heading(col, text=d_headings[col])
            d_tree.column(col, width=d_widths[col], anchor="w" if col == "pump" else "center")
        for d in diesel_entries:
            d_tree.insert("", "end", values=(d["diesel_type"], d["liters"], f'{d["rate_per_liter"]:,.0f}', f'{d["total_cost"]:,.0f}', d["pump_location"] or "", d["diesel_date"]))
        d_tree.pack(fill="x", padx=20, pady=(0, 15))
        if not diesel_entries:
            tk.Label(diesel_card, text="No diesel entries recorded for this trip.", bg=COLOR_CARD_BG, fg="#6B7280", font=FONT_LABEL).pack(anchor="w", padx=20, pady=(0, 10))

        # ---- Totals Summary ----
        totals = compute_trip_totals(trip)
        summary_card = tk.Frame(self.ledger_frame, bg=COLOR_CARD_BG)
        summary_card.pack(fill="x", pady=(0, 20))
        tk.Label(
            summary_card, text="Trip Summary", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=20, pady=(15, 10))

        summary_grid = tk.Frame(summary_card, bg=COLOR_CARD_BG)
        summary_grid.pack(fill="x", padx=20, pady=(0, 20))

        rows = [
            ("Total Brokery", trip["total_brokery"], COLOR_TEXT_DARK),
            ("Wasool Kiraya (Received)", totals["wasool_kiraya"], COLOR_SUCCESS),
            ("Remaining Kiraya", trip["remaining_kiraya"], COLOR_DANGER),
            ("Total Expenses", totals["total_expenses"], COLOR_DANGER),
            ("Total Diesel Cost", totals["total_diesel"], COLOR_DANGER),
            ("Daily Wages", totals["daily_wages"], COLOR_DANGER),
            ("TOTAL COST (Expenses+Diesel+Wages)", totals["total_cost"], COLOR_DANGER),
        ]
        for i, (label, value, color) in enumerate(rows):
            tk.Label(summary_grid, text=f"{label}:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
                .grid(row=i, column=0, sticky="w", pady=3)
            tk.Label(summary_grid, text=f"Rs {value:,.0f}", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG, fg=color)\
                .grid(row=i, column=1, sticky="w", padx=(10, 0), pady=3)

        net_color = COLOR_SUCCESS if totals["net_saving"] >= 0 else COLOR_DANGER
        net_label_text = "NET SAVING" if totals["net_saving"] >= 0 else "NET LOSS"
        tk.Label(
            summary_grid, text=f"{net_label_text}:", font=FONT_CARD_VALUE, bg=COLOR_CARD_BG
        ).grid(row=len(rows), column=0, sticky="w", pady=(10, 0))
        tk.Label(
            summary_grid, text=f"Rs {abs(totals['net_saving']):,.0f}", font=FONT_CARD_VALUE,
            bg=COLOR_CARD_BG, fg=net_color
        ).grid(row=len(rows), column=1, sticky="w", padx=(10, 0), pady=(10, 0))
