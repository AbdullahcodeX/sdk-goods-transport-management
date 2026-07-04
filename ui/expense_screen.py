"""
SDK GOODS - Goods Transport Management System
Expense Screen
--------------------------------
For a selected vehicle -> selected trip: add Fixed or Other
expenses (Tools, Food, Tyre, Police, Inaam, Motorway Toll,
GT Road Toll, Vehicle Work Cost, Other) and see the running total.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from models.vehicle_model import get_all_vehicles
from models.trip_model import get_trips_by_vehicle
from models.expense_model import add_expense, get_expenses_by_trip, delete_expense, get_total_expenses_by_trip
from ui.widgets.styled_widgets import (
    COLOR_CONTENT_BG, COLOR_CARD_BG, COLOR_TEXT_DARK, COLOR_HEADER_BG,
    COLOR_DANGER, FONT_HEADER, FONT_LABEL, FONT_LABEL_BOLD, FONT_CARD_VALUE,
)
from utils.constants import EXPENSE_GROUPS, FIXED_EXPENSE_CATEGORIES, OTHER_EXPENSE_CATEGORIES


class ExpenseScreen(tk.Frame):
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
            card, text="Add Expense", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).grid(row=0, column=0, columnspan=5, sticky="w", padx=20, pady=(15, 15))

        tk.Label(card, text="Expense Group:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=1, column=0, sticky="w", padx=20, pady=6)
        self.group_var = tk.StringVar(value=EXPENSE_GROUPS[0])
        self.group_combo = ttk.Combobox(
            card, textvariable=self.group_var, values=EXPENSE_GROUPS, state="readonly", width=15
        )
        self.group_combo.grid(row=1, column=1, sticky="w", pady=6)
        self.group_combo.bind("<<ComboboxSelected>>", lambda e: self.update_category_options())

        tk.Label(card, text="Category:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=1, column=2, sticky="w", padx=(20, 5), pady=6)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            card, textvariable=self.category_var, values=FIXED_EXPENSE_CATEGORIES, state="readonly", width=28
        )
        self.category_combo.grid(row=1, column=3, sticky="w", pady=6)
        self.category_combo.current(0)

        tk.Label(card, text="Amount (Rs):", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=2, column=0, sticky="w", padx=20, pady=6)
        self.amount_entry = tk.Entry(card, font=FONT_LABEL, width=15)
        self.amount_entry.grid(row=2, column=1, sticky="w", pady=6)

        tk.Label(card, text="Date (YYYY-MM-DD):", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=2, column=2, sticky="w", padx=(20, 5), pady=6)
        self.date_entry = tk.Entry(card, font=FONT_LABEL, width=15)
        self.date_entry.insert(0, datetime.date.today().isoformat())
        self.date_entry.grid(row=2, column=3, sticky="w", pady=6)

        tk.Label(card, text="Description:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=3, column=0, sticky="w", padx=20, pady=6)
        self.description_entry = tk.Entry(card, font=FONT_LABEL, width=60)
        self.description_entry.grid(row=3, column=1, columnspan=3, sticky="w", pady=6)

        btn_frame = tk.Frame(card, bg=COLOR_CARD_BG)
        btn_frame.grid(row=4, column=0, columnspan=5, sticky="w", padx=20, pady=(10, 20))
        tk.Button(
            btn_frame, text="Add Expense", bg=COLOR_HEADER_BG, fg="white", font=FONT_LABEL_BOLD,
            padx=16, pady=7, bd=0, cursor="hand2", command=self.add_expense_click
        ).pack(side="left")

    def update_category_options(self):
        if self.group_var.get() == "Fixed":
            self.category_combo.configure(values=FIXED_EXPENSE_CATEGORIES)
        else:
            self.category_combo.configure(values=OTHER_EXPENSE_CATEGORIES)
        self.category_combo.current(0)

    # ---------------------------------------------------------
    def _build_table(self):
        card = tk.Frame(self, bg=COLOR_CARD_BG)
        card.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        tk.Label(
            card, text="Expenses for Selected Trip", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=20, pady=(15, 10))

        columns = ("id", "group", "category", "amount", "description", "date")
        headings = {
            "id": "ID", "group": "Group", "category": "Category",
            "amount": "Amount", "description": "Description", "date": "Date"
        }
        widths = {"id": 40, "group": 70, "category": 190, "amount": 100, "description": 220, "date": 100}

        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col],
                              anchor="w" if col in ("category", "description") else "center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        action_frame = tk.Frame(card, bg=COLOR_CARD_BG)
        action_frame.pack(fill="x", padx=20, pady=(0, 10))
        tk.Button(
            action_frame, text="Delete Selected Expense", command=self.delete_selected_expense,
            bg=COLOR_DANGER, fg="white", font=FONT_LABEL_BOLD, bd=0, padx=14, pady=6, cursor="hand2"
        ).pack(side="left")

        self.total_label = tk.Label(
            card, text="Total Expenses: Rs 0", bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK, font=FONT_CARD_VALUE
        )
        self.total_label.pack(anchor="w", padx=20, pady=(0, 15))

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        trip = self.get_selected_trip()
        if not trip:
            self.total_label.configure(text="Total Expenses: Rs 0")
            return
        for e in get_expenses_by_trip(trip["id"]):
            self.tree.insert("", "end", values=(
                e["id"], e["expense_group"], e["category"],
                f'{e["amount"]:,.0f}', e["description"] or "", e["expense_date"]
            ))
        total = get_total_expenses_by_trip(trip["id"])
        self.total_label.configure(text=f"Total Expenses: Rs {total:,.0f}")

    def get_selected_expense_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    def delete_selected_expense(self):
        eid = self.get_selected_expense_id()
        if not eid:
            messagebox.showwarning("No Selection", "Please select an expense row first.")
            return
        if messagebox.askyesno("Confirm Delete", "Delete this expense entry?"):
            delete_expense(eid)
            self.refresh_table()

    def add_expense_click(self):
        trip = self.get_selected_trip()
        if not trip:
            messagebox.showerror("Error", "Please select a vehicle and trip first.")
            return

        category = self.category_var.get().strip()
        if not category:
            messagebox.showerror("Validation Error", "Please select a category.")
            return

        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Amount must be a positive number.")
            return

        date_val = self.date_entry.get().strip()
        if not date_val:
            messagebox.showerror("Validation Error", "Date is required.")
            return

        add_expense(
            trip_id=trip["id"], expense_group=self.group_var.get(),
            category=category, amount=amount,
            description=self.description_entry.get().strip(), expense_date=date_val
        )
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.refresh_table()
