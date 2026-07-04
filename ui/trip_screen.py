"""
SDK GOODS - Goods Transport Management System
Trip Screen
--------------------------------
For a selected vehicle: add/edit/delete trips with full details
(date, from/to city, goods, broker, station, brokery, wasool kiraya,
auto remaining kiraya, daily wages, weight).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from models.vehicle_model import get_all_vehicles
from models.trip_model import add_trip, get_trips_by_vehicle, get_trip, update_trip, delete_trip
from ui.widgets.city_selector import CitySelector
from ui.widgets.styled_widgets import (
    COLOR_CONTENT_BG, COLOR_CARD_BG, COLOR_TEXT_DARK, COLOR_HEADER_BG,
    COLOR_DANGER, COLOR_SUCCESS, FONT_HEADER, FONT_LABEL, FONT_LABEL_BOLD,
)
from utils.constants import WEIGHT_UNITS


class TripScreen(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_CONTENT_BG, **kwargs)
        self.selected_trip_id = None
        self.vehicles = get_all_vehicles()

        if not self.vehicles:
            tk.Label(
                self, text="No vehicles found. Please add a vehicle first in the Vehicles screen.",
                bg=COLOR_CONTENT_BG, fg=COLOR_DANGER, font=FONT_HEADER
            ).pack(pady=40)
            return

        self._build_vehicle_selector()
        self._build_form()
        self._build_table()
        self.refresh_table()

    # ---------------------------------------------------------
    def _build_vehicle_selector(self):
        frame = tk.Frame(self, bg=COLOR_CONTENT_BG)
        frame.pack(fill="x", padx=25, pady=(20, 5))

        tk.Label(
            frame, text="Select Vehicle:", bg=COLOR_CONTENT_BG, font=FONT_LABEL_BOLD
        ).pack(side="left", padx=(0, 10))

        self.vehicle_labels = [f'{v["vehicle_number"]} ({v["city"]})' for v in self.vehicles]
        self.vehicle_var = tk.StringVar()
        self.vehicle_combo = ttk.Combobox(
            frame, textvariable=self.vehicle_var, values=self.vehicle_labels,
            state="readonly", width=35
        )
        self.vehicle_combo.pack(side="left")
        self.vehicle_combo.current(0)
        self.vehicle_combo.bind("<<ComboboxSelected>>", lambda e: (self.clear_form(), self.refresh_table()))

    def get_selected_vehicle(self):
        idx = self.vehicle_combo.current()
        if idx < 0 or idx >= len(self.vehicles):
            return None
        return self.vehicles[idx]

    # ---------------------------------------------------------
    def _build_form(self):
        card = tk.Frame(self, bg=COLOR_CARD_BG)
        card.pack(fill="x", padx=25, pady=10)

        tk.Label(
            card, text="Add / Edit Trip", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).grid(row=0, column=0, columnspan=6, sticky="w", padx=20, pady=(15, 15))

        r = 1
        tk.Label(card, text="Trip Date (YYYY-MM-DD):", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=0, sticky="w", padx=20, pady=6)
        self.date_entry = tk.Entry(card, font=FONT_LABEL, width=15)
        self.date_entry.insert(0, datetime.date.today().isoformat())
        self.date_entry.grid(row=r, column=1, sticky="w", pady=6)

        tk.Label(card, text="Weight:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=2, sticky="w", padx=(20, 5), pady=6)
        self.weight_entry = tk.Entry(card, font=FONT_LABEL, width=10)
        self.weight_entry.insert(0, "0")
        self.weight_entry.grid(row=r, column=3, sticky="w", pady=6)

        self.weight_unit_var = tk.StringVar(value=WEIGHT_UNITS[0])
        ttk.Combobox(
            card, textvariable=self.weight_unit_var, values=WEIGHT_UNITS,
            state="readonly", width=8
        ).grid(row=r, column=4, sticky="w", pady=6)

        r += 1
        tk.Label(card, text="From City:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=0, sticky="w", padx=20, pady=6)
        self.from_city = CitySelector(card, bg=COLOR_CARD_BG)
        self.from_city.grid(row=r, column=1, sticky="w", pady=6)

        tk.Label(card, text="To City:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=2, sticky="w", padx=(20, 5), pady=6)
        self.to_city = CitySelector(card, bg=COLOR_CARD_BG)
        self.to_city.grid(row=r, column=3, columnspan=2, sticky="w", pady=6)

        r += 1
        tk.Label(card, text="Goods / Maal Details:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=0, sticky="w", padx=20, pady=6)
        self.goods_entry = tk.Entry(card, font=FONT_LABEL, width=60)
        self.goods_entry.grid(row=r, column=1, columnspan=4, sticky="w", pady=6)

        r += 1
        tk.Label(card, text="Broker Name:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=0, sticky="w", padx=20, pady=6)
        self.broker_name_entry = tk.Entry(card, font=FONT_LABEL, width=25)
        self.broker_name_entry.grid(row=r, column=1, sticky="w", pady=6)

        tk.Label(card, text="Broker Contact:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=2, sticky="w", padx=(20, 5), pady=6)
        self.broker_contact_entry = tk.Entry(card, font=FONT_LABEL, width=20)
        self.broker_contact_entry.grid(row=r, column=3, sticky="w", pady=6)

        r += 1
        tk.Label(card, text="Station Details:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=0, sticky="w", padx=20, pady=6)
        self.station_entry = tk.Entry(card, font=FONT_LABEL, width=60)
        self.station_entry.grid(row=r, column=1, columnspan=4, sticky="w", pady=6)

        r += 1
        tk.Label(card, text="Total Brokery (Rs):", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=0, sticky="w", padx=20, pady=6)
        self.total_brokery_entry = tk.Entry(card, font=FONT_LABEL, width=15)
        self.total_brokery_entry.insert(0, "0")
        self.total_brokery_entry.grid(row=r, column=1, sticky="w", pady=6)
        self.total_brokery_entry.bind("<KeyRelease>", lambda e: self.update_remaining_preview())

        tk.Label(card, text="Wasool Kiraya (Rs):", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=2, sticky="w", padx=(20, 5), pady=6)
        self.wasool_kiraya_entry = tk.Entry(card, font=FONT_LABEL, width=15)
        self.wasool_kiraya_entry.insert(0, "0")
        self.wasool_kiraya_entry.grid(row=r, column=3, sticky="w", pady=6)
        self.wasool_kiraya_entry.bind("<KeyRelease>", lambda e: self.update_remaining_preview())

        r += 1
        tk.Label(card, text="Remaining Kiraya (auto):", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=0, sticky="w", padx=20, pady=6)
        self.remaining_label = tk.Label(
            card, text="0", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG, fg=COLOR_DANGER
        )
        self.remaining_label.grid(row=r, column=1, sticky="w", pady=6)

        tk.Label(card, text="Daily Wages (Rs):", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=2, sticky="w", padx=(20, 5), pady=6)
        self.daily_wages_entry = tk.Entry(card, font=FONT_LABEL, width=15)
        self.daily_wages_entry.insert(0, "0")
        self.daily_wages_entry.grid(row=r, column=3, sticky="w", pady=6)

        r += 1
        tk.Label(card, text="Notes:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=r, column=0, sticky="w", padx=20, pady=6)
        self.notes_entry = tk.Entry(card, font=FONT_LABEL, width=60)
        self.notes_entry.grid(row=r, column=1, columnspan=4, sticky="w", pady=6)

        r += 1
        btn_frame = tk.Frame(card, bg=COLOR_CARD_BG)
        btn_frame.grid(row=r, column=0, columnspan=6, sticky="w", padx=20, pady=(10, 20))

        self.save_btn = tk.Button(
            btn_frame, text="Add Trip", bg=COLOR_HEADER_BG, fg="white", font=FONT_LABEL_BOLD,
            padx=16, pady=7, bd=0, cursor="hand2", command=self.save_trip
        )
        self.save_btn.pack(side="left", padx=(0, 10))

        tk.Button(
            btn_frame, text="Clear / New", bg="#9CA3AF", fg="white", font=FONT_LABEL_BOLD,
            padx=16, pady=7, bd=0, cursor="hand2", command=self.clear_form
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_frame, text="Delete Selected Trip", bg=COLOR_DANGER, fg="white", font=FONT_LABEL_BOLD,
            padx=16, pady=7, bd=0, cursor="hand2", command=self.delete_selected_trip
        ).pack(side="left")

        self.update_remaining_preview()

    def update_remaining_preview(self):
        try:
            total_brokery = float(self.total_brokery_entry.get() or 0)
            wasool = float(self.wasool_kiraya_entry.get() or 0)
            remaining = total_brokery - wasool
            color = COLOR_DANGER if remaining > 0 else COLOR_SUCCESS
            self.remaining_label.configure(text=f"Rs {remaining:,.0f}", fg=color)
        except ValueError:
            self.remaining_label.configure(text="Invalid number", fg=COLOR_DANGER)

    # ---------------------------------------------------------
    def _build_table(self):
        card = tk.Frame(self, bg=COLOR_CARD_BG)
        card.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        tk.Label(
            card, text="Trips for Selected Vehicle", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=20, pady=(15, 10))

        columns = ("id", "receipt_no", "trip_date", "route", "brokery", "wasool", "remaining", "wages")
        headings = {
            "id": "ID", "receipt_no": "Receipt #", "trip_date": "Date", "route": "Route",
            "brokery": "Brokery", "wasool": "Wasool Kiraya", "remaining": "Remaining", "wages": "Wages"
        }
        widths = {
            "id": 40, "receipt_no": 100, "trip_date": 100, "route": 200,
            "brokery": 100, "wasool": 110, "remaining": 100, "wages": 90
        }

        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w" if col == "route" else "center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        action_frame = tk.Frame(card, bg=COLOR_CARD_BG)
        action_frame.pack(fill="x", padx=20, pady=(0, 15))
        tk.Button(
            action_frame, text="Load Selected for Edit", command=self.load_selected_for_edit,
            bg=COLOR_HEADER_BG, fg="white", font=FONT_LABEL_BOLD, bd=0, padx=14, pady=6, cursor="hand2"
        ).pack(side="left")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        vehicle = self.get_selected_vehicle()
        if not vehicle:
            return
        trips = get_trips_by_vehicle(vehicle["id"])
        for t in trips:
            route = f'{t["from_city"]} -> {t["to_city"]}'
            self.tree.insert("", "end", values=(
                t["id"], t["receipt_no"], t["trip_date"], route,
                f'{t["total_brokery"]:,.0f}', f'{t["wasool_kiraya"]:,.0f}',
                f'{t["remaining_kiraya"]:,.0f}', f'{t["daily_wages"]:,.0f}'
            ))

    # ---------------------------------------------------------
    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    def load_selected_for_edit(self):
        tid = self.get_selected_id()
        if not tid:
            messagebox.showwarning("No Selection", "Please select a trip from the table first.")
            return
        t = get_trip(tid)
        if not t:
            return

        self.selected_trip_id = tid
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, t["trip_date"])
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, str(t["weight"]))
        self.weight_unit_var.set(t["weight_unit"])
        self.from_city.set_value(t["from_city"])
        self.to_city.set_value(t["to_city"])
        self.goods_entry.delete(0, tk.END)
        self.goods_entry.insert(0, t["goods_details"] or "")
        self.broker_name_entry.delete(0, tk.END)
        self.broker_name_entry.insert(0, t["broker_name"] or "")
        self.broker_contact_entry.delete(0, tk.END)
        self.broker_contact_entry.insert(0, t["broker_contact"] or "")
        self.station_entry.delete(0, tk.END)
        self.station_entry.insert(0, t["station_details"] or "")
        self.total_brokery_entry.delete(0, tk.END)
        self.total_brokery_entry.insert(0, str(t["total_brokery"]))
        self.wasool_kiraya_entry.delete(0, tk.END)
        self.wasool_kiraya_entry.insert(0, str(t["wasool_kiraya"]))
        self.daily_wages_entry.delete(0, tk.END)
        self.daily_wages_entry.insert(0, str(t["daily_wages"]))
        self.notes_entry.delete(0, tk.END)
        self.notes_entry.insert(0, t["notes"] or "")

        self.update_remaining_preview()
        self.save_btn.configure(text="Update Trip")

    def delete_selected_trip(self):
        tid = self.get_selected_id()
        if not tid:
            messagebox.showwarning("No Selection", "Please select a trip from the table first.")
            return
        if messagebox.askyesno(
            "Confirm Delete",
            "Deleting this trip will also permanently delete all its expense and diesel records.\n\nContinue?"
        ):
            delete_trip(tid)
            self.clear_form()
            self.refresh_table()

    # ---------------------------------------------------------
    def clear_form(self):
        self.selected_trip_id = None
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.date.today().isoformat())
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, "0")
        self.weight_unit_var.set(WEIGHT_UNITS[0])
        self.from_city.reset()
        self.to_city.reset()
        self.goods_entry.delete(0, tk.END)
        self.broker_name_entry.delete(0, tk.END)
        self.broker_contact_entry.delete(0, tk.END)
        self.station_entry.delete(0, tk.END)
        self.total_brokery_entry.delete(0, tk.END)
        self.total_brokery_entry.insert(0, "0")
        self.wasool_kiraya_entry.delete(0, tk.END)
        self.wasool_kiraya_entry.insert(0, "0")
        self.daily_wages_entry.delete(0, tk.END)
        self.daily_wages_entry.insert(0, "0")
        self.notes_entry.delete(0, tk.END)
        self.update_remaining_preview()
        self.save_btn.configure(text="Add Trip")

    def save_trip(self):
        vehicle = self.get_selected_vehicle()
        if not vehicle:
            messagebox.showerror("Error", "Please select a vehicle first.")
            return

        trip_date = self.date_entry.get().strip()
        from_city = self.from_city.get_value().strip()
        to_city = self.to_city.get_value().strip()

        if not trip_date:
            messagebox.showerror("Validation Error", "Trip date is required.")
            return
        if not from_city or not to_city:
            messagebox.showerror("Validation Error", "Please select or type both From City and To City.")
            return

        try:
            weight = float(self.weight_entry.get() or 0)
            total_brokery = float(self.total_brokery_entry.get() or 0)
            wasool_kiraya = float(self.wasool_kiraya_entry.get() or 0)
            daily_wages = float(self.daily_wages_entry.get() or 0)
        except ValueError:
            messagebox.showerror("Validation Error", "Weight, Brokery, Wasool Kiraya, and Wages must be numbers.")
            return

        kwargs = dict(
            trip_date=trip_date, from_city=from_city, to_city=to_city,
            goods_details=self.goods_entry.get().strip(),
            weight=weight, weight_unit=self.weight_unit_var.get(),
            broker_name=self.broker_name_entry.get().strip(),
            broker_contact=self.broker_contact_entry.get().strip(),
            station_details=self.station_entry.get().strip(),
            total_brokery=total_brokery, wasool_kiraya=wasool_kiraya,
            daily_wages=daily_wages, notes=self.notes_entry.get().strip(),
        )

        if self.selected_trip_id:
            update_trip(self.selected_trip_id, **kwargs)
            messagebox.showinfo("Success", "Trip updated successfully.")
        else:
            add_trip(vehicle_id=vehicle["id"], **kwargs)
            messagebox.showinfo("Success", "Trip added successfully.")

        self.clear_form()
        self.refresh_table()
