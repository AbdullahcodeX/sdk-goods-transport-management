"""
SDK GOODS - Goods Transport Management System
Diesel Screen
--------------------------------
For a selected vehicle -> selected trip: record diesel purchases
(Irani / Pakistani / Other), with auto-calculated total cost.
"""

import tkinter as tk , tkinter
from tkinter import ttk, messagebox
import datetime

from models.vehicle_model import get_all_vehicles
from models.trip_model import get_trips_by_vehicle
from models.diesel_model import add_diesel, get_diesel_by_trip, delete_diesel, get_total_diesel_by_trip
from ui.widgets.styled_widgets import (
    COLOR_CONTENT_BG, COLOR_CARD_BG, COLOR_TEXT_DARK, COLOR_HEADER_BG,
    COLOR_DANGER, FONT_HEADER, FONT_LABEL, FONT_LABEL_BOLD, FONT_CARD_VALUE,
)
from utils.constants import DIESEL_TYPES


class DieselScreen(tk.Frame):
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
        self._build_form()
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

        tk.Label(frame, text="Trip:", bg=COLOR_CONTENT_BG, font=FONT_LABEL_BOLD).pack(side="left", padx=(0, 8))
        self.trip_var = tk.StringVar()
        self.trip_combo = ttk.Combobox(frame, textvariable=self.trip_var, values=[], state="readonly", width=45)
        self.trip_combo.pack(side="left")
        self.trip_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

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
        self.refresh_table()

    def get_selected_trip(self):
        idx = self.trip_combo.current()
        if idx < 0 or idx >= len(self.trips):
            return None
        return self.trips[idx]

    # ---------------------------------------------------------
    def _build_form(self):
        card = tk.Frame(self, bg=COLOR_CARD_BG)
        card.pack(fill="x", padx=25, pady=10)

        tk.Label(
            card, text="Add Diesel Entry", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).grid(row=0, column=0, columnspan=5, sticky="w", padx=20, pady=(15, 15))

        tk.Label(card, text="Diesel Type:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=1, column=0, sticky="w", padx=20, pady=6)
        self.diesel_type_var = tk.StringVar(value=DIESEL_TYPES[0])
        ttk.Combobox(
            card, textvariable=self.diesel_type_var, values=DIESEL_TYPES, state="readonly", width=20
        ).grid(row=1, column=1, sticky="w", pady=6)

        tk.Label(card, text="Liters:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=1, column=2, sticky="w", padx=(20, 5), pady=6)
        self.liters_entry = tk.Entry(card, font=FONT_LABEL, width=12)
        self.liters_entry.grid(row=1, column=3, sticky="w", pady=6)
        self.liters_entry.bind("<KeyRelease>", lambda e: self.update_total_preview())

        tk.Label(card, text="Rate / Liter (Rs):", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=2, column=0, sticky="w", padx=20, pady=6)
        self.rate_entry = tk.Entry(card, font=FONT_LABEL, width=12)
        self.rate_entry.grid(row=2, column=1, sticky="w", pady=6)
        self.rate_entry.bind("<KeyRelease>", lambda e: self.update_total_preview())

        tk.Label(card, text="Total Cost (auto):", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=2, column=2, sticky="w", padx=(20, 5), pady=6)
        self.total_cost_label = tk.Label(card, text="Rs 0", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK)
        self.total_cost_label.grid(row=2, column=3, sticky="w", pady=6)

        tk.Label(card, text="Pump / Location:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=3, column=0, sticky="w", padx=20, pady=6)
        self.pump_entry = tk.Entry(card, font=FONT_LABEL, width=30)
        self.pump_entry.grid(row=3, column=1, columnspan=2, sticky="w", pady=6)

        tk.Label(card, text="Date (YYYY-MM-DD):", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=3, column=3, sticky="w", padx=(0, 5), pady=6)
        self.date_entry = tk.Entry(card, font=FONT_LABEL, width=15)
        self.date_entry.insert(0, datetime.date.today().isoformat())
        self.date_entry.grid(row=3, column=4, sticky="w", pady=6)

        btn_frame = tk.Frame(card, bg=COLOR_CARD_BG)
        btn_frame.grid(row=4, column=0, columnspan=5, sticky="w", padx=20, pady=(10, 20))
        tk.Button(
            btn_frame, text="Add Diesel Entry", bg=COLOR_HEADER_BG, fg="white", font=FONT_LABEL_BOLD,
            padx=16, pady=7, bd=0, cursor="hand2", command=self.add_diesel_click
        ).pack(side="left")

    def update_total_preview(self):
        try:
            liters = float(self.liters_entry.get() or 0)
            rate = float(self.rate_entry.get() or 0)
            self.total_cost_label.configure(text=f"Rs {liters * rate:,.0f}")
        except ValueError:
            self.total_cost_label.configure(text="Invalid number")

    # ---------------------------------------------------------
    def _build_table(self):
        card = tk.Frame(self, bg=COLOR_CARD_BG)
        card.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        tk.Label(
            card, text="Diesel Entries for Selected Trip", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=20, pady=(15, 10))

        columns = ("id", "type", "liters", "rate", "total", "pump", "date")
        headings = {
            "id": "ID", "type": "Type", "liters": "Liters", "rate": "Rate/Liter",
            "total": "Total Cost", "pump": "Pump/Location", "date": "Date"
        }
        widths = {"id": 40, "type": 130, "liters": 70, "rate": 90, "total": 100, "pump": 180, "date": 100}

        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w" if col == "pump" else "center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        action_frame = tk.Frame(card, bg=COLOR_CARD_BG)
        action_frame.pack(fill="x", padx=20, pady=(0, 10))
        tk.Button(
            action_frame, text="Delete Selected Entry", command=self.delete_selected_diesel,
            bg=COLOR_DANGER, fg="white", font=FONT_LABEL_BOLD, bd=0, padx=14, pady=6, cursor="hand2"
        ).pack(side="left")

        self.total_label = tk.Label(
            card, text="Total Diesel Cost: Rs 0", bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK, font=FONT_CARD_VALUE
        )
        self.total_label.pack(anchor="w", padx=20, pady=(0, 15))

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        trip = self.get_selected_trip()
        if not trip:
            self.total_label.configure(text="Total Diesel Cost: Rs 0")
            return
        for d in get_diesel_by_trip(trip["id"]):
            self.tree.insert("", "end", values=(
                d["id"], d["diesel_type"], d["liters"], f'{d["rate_per_liter"]:,.0f}',
                f'{d["total_cost"]:,.0f}', d["pump_location"] or "", d["diesel_date"]
            ))
        total = get_total_diesel_by_trip(trip["id"])
        self.total_label.configure(text=f"Total Diesel Cost: Rs {total:,.0f}")

    def get_selected_diesel_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    def delete_selected_diesel(self):
        did = self.get_selected_diesel_id()
        if not did:
            messagebox.showwarning("No Selection", "Please select a diesel entry first.")
            return
        if messagebox.askyesno("Confirm Delete", "Delete this diesel entry?"):
            delete_diesel(did)
            self.refresh_table()

    def add_diesel_click(self):
        trip = self.get_selected_trip()
        if not trip:
            messagebox.showerror("Error", "Please select a vehicle and trip first.")
            return

        try:
            liters = float(self.liters_entry.get())
            rate = float(self.rate_entry.get())
            if liters <= 0 or rate <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Liters and Rate must be positive numbers.")
            return

        date_val = self.date_entry.get().strip()
        if not date_val:
            messagebox.showerror("Validation Error", "Date is required.")
            return

        total_cost = liters * rate
        add_diesel(
            trip_id=trip["id"], diesel_type=self.diesel_type_var.get(),
            liters=liters, rate_per_liter=rate, total_cost=total_cost,
            pump_location=self.pump_entry.get().strip(), diesel_date=date_val
        )
        self.liters_entry.delete(0, tk.END)
        self.rate_entry.delete(0, tk.END)
        self.pump_entry.delete(0, tk.END)
        self.total_cost_label.configure(text="Rs 0")
        self.refresh_table()
