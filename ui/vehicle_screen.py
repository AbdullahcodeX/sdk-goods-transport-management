"""
SDK GOODS - Goods Transport Management System
Vehicle Screen
--------------------------------
Fully working screen to:
  - Add a new vehicle (vehicle number + city dropdown/"Other" + status)
  - View all vehicles in a table
  - Edit an existing vehicle
  - Activate / Deactivate a vehicle (soft toggle, history is preserved)
  - Search/filter vehicles by number or city
"""

import tkinter as tk
from tkinter import ttk, messagebox

from models.vehicle_model import (
    add_vehicle, get_all_vehicles, get_vehicle,
    update_vehicle, set_vehicle_status,
)
from ui.widgets.city_selector import CitySelector
from ui.widgets.styled_widgets import (
    COLOR_CONTENT_BG, COLOR_CARD_BG, COLOR_TEXT_DARK, COLOR_HEADER_BG,
    COLOR_DANGER, COLOR_SUCCESS, FONT_HEADER, FONT_LABEL, FONT_LABEL_BOLD,
)
from utils.constants import VEHICLE_STATUS_OPTIONS


class VehicleScreen(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_CONTENT_BG, **kwargs)
        self.selected_vehicle_id = None

        self._build_form()
        self._build_search_bar()
        self._build_table()
        self.refresh_table()

    # ---------------------------------------------------------
    # FORM: Add / Edit vehicle
    # ---------------------------------------------------------
    def _build_form(self):
        form_card = tk.Frame(self, bg=COLOR_CARD_BG, bd=0)
        form_card.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(
            form_card, text="Add / Edit Vehicle", bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_DARK, font=FONT_HEADER
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(15, 15))

        # Vehicle Number
        tk.Label(
            form_card, text="Vehicle Number:", bg=COLOR_CARD_BG, font=FONT_LABEL_BOLD
        ).grid(row=1, column=0, sticky="w", padx=(20, 5), pady=8)
        self.vehicle_number_entry = tk.Entry(form_card, font=FONT_LABEL, width=25)
        self.vehicle_number_entry.grid(row=1, column=1, sticky="w", pady=8)

        # City
        tk.Label(
            form_card, text="City:", bg=COLOR_CARD_BG, font=FONT_LABEL_BOLD
        ).grid(row=1, column=2, sticky="w", padx=(30, 5), pady=8)
        self.city_selector = CitySelector(form_card, bg=COLOR_CARD_BG)
        self.city_selector.grid(row=1, column=3, sticky="w", pady=8)

        # Status
        tk.Label(
            form_card, text="Status:", bg=COLOR_CARD_BG, font=FONT_LABEL_BOLD
        ).grid(row=2, column=0, sticky="w", padx=(20, 5), pady=8)
        self.status_var = tk.StringVar(value=VEHICLE_STATUS_OPTIONS[0])
        self.status_combo = ttk.Combobox(
            form_card, textvariable=self.status_var, values=VEHICLE_STATUS_OPTIONS,
            state="readonly", width=22
        )
        self.status_combo.grid(row=2, column=1, sticky="w", pady=8)

        # Buttons
        btn_frame = tk.Frame(form_card, bg=COLOR_CARD_BG)
        btn_frame.grid(row=3, column=0, columnspan=4, sticky="w", padx=20, pady=(10, 20))

        self.save_btn = tk.Button(
            btn_frame, text="Add Vehicle", bg=COLOR_HEADER_BG, fg="white",
            font=FONT_LABEL_BOLD, padx=16, pady=7, bd=0, cursor="hand2",
            command=self.save_vehicle
        )
        self.save_btn.pack(side="left", padx=(0, 10))

        tk.Button(
            btn_frame, text="Clear / New", bg="#9CA3AF", fg="white",
            font=FONT_LABEL_BOLD, padx=16, pady=7, bd=0, cursor="hand2",
            command=self.clear_form
        ).pack(side="left")

    # ---------------------------------------------------------
    # SEARCH BAR
    # ---------------------------------------------------------
    def _build_search_bar(self):
        search_frame = tk.Frame(self, bg=COLOR_CONTENT_BG)
        search_frame.pack(fill="x", padx=25, pady=(0, 5))

        tk.Label(
            search_frame, text="Search:", bg=COLOR_CONTENT_BG, font=FONT_LABEL_BOLD
        ).pack(side="left", padx=(0, 8))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=FONT_LABEL, width=30)
        search_entry.pack(side="left", padx=(0, 8))
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_table())

        tk.Button(
            search_frame, text="Clear Search", bg="#9CA3AF", fg="white",
            font=FONT_LABEL, padx=10, pady=3, bd=0, cursor="hand2",
            command=self.clear_search
        ).pack(side="left")

    def clear_search(self):
        self.search_var.set("")
        self.refresh_table()

    # ---------------------------------------------------------
    # TABLE: All vehicles
    # ---------------------------------------------------------
    def _build_table(self):
        table_card = tk.Frame(self, bg=COLOR_CARD_BG)
        table_card.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        tk.Label(
            table_card, text="All Vehicles", bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_DARK, font=FONT_HEADER
        ).pack(anchor="w", padx=20, pady=(15, 10))

        columns = ("id", "vehicle_number", "city", "status", "created_at")
        headings = {
            "id": "ID", "vehicle_number": "Vehicle Number", "city": "City",
            "status": "Status", "created_at": "Added On"
        }
        widths = {"id": 50, "vehicle_number": 200, "city": 200, "status": 130, "created_at": 170}

        style = ttk.Style()
        style.configure("Vehicle.Treeview", rowheight=28, font=("Segoe UI", 10))
        style.configure("Vehicle.Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.tree = ttk.Treeview(
            table_card, columns=columns, show="headings", height=12,
            style="Vehicle.Treeview"
        )
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col],
                              anchor="w" if col in ("vehicle_number", "city") else "center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Color tags for status
        self.tree.tag_configure("active", foreground=COLOR_SUCCESS)
        self.tree.tag_configure("inactive", foreground=COLOR_DANGER)
        self.tree.tag_configure("workshop", foreground="#B45309")

        action_frame = tk.Frame(table_card, bg=COLOR_CARD_BG)
        action_frame.pack(fill="x", padx=20, pady=(0, 15))

        tk.Button(
            action_frame, text="Edit Selected", command=self.load_selected_for_edit,
            bg=COLOR_HEADER_BG, fg="white", font=FONT_LABEL_BOLD, bd=0,
            padx=14, pady=6, cursor="hand2"
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            action_frame, text="Activate / Deactivate", command=self.toggle_status,
            bg=COLOR_DANGER, fg="white", font=FONT_LABEL_BOLD, bd=0,
            padx=14, pady=6, cursor="hand2"
        ).pack(side="left")

        total_label_frame = tk.Frame(table_card, bg=COLOR_CARD_BG)
        total_label_frame.pack(fill="x", padx=20, pady=(0, 15))
        self.total_label = tk.Label(
            total_label_frame, text="", bg=COLOR_CARD_BG, fg="#6B7280", font=FONT_LABEL
        )
        self.total_label.pack(side="left")

    # ---------------------------------------------------------
    # DATA REFRESH
    # ---------------------------------------------------------
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        search_text = self.search_var.get().strip() if hasattr(self, "search_var") else None
        vehicles = get_all_vehicles(search_text if search_text else None)

        for v in vehicles:
            tag = "active"
            if v["status"] == "Inactive":
                tag = "inactive"
            elif v["status"] == "In Workshop":
                tag = "workshop"
            self.tree.insert(
                "", "end",
                values=(v["id"], v["vehicle_number"], v["city"], v["status"], v["created_at"]),
                tags=(tag,)
            )

        self.total_label.configure(text=f"Total vehicles shown: {len(vehicles)}")

    # ---------------------------------------------------------
    # SELECTION HELPERS
    # ---------------------------------------------------------
    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    def load_selected_for_edit(self):
        vid = self.get_selected_id()
        if not vid:
            messagebox.showwarning("No Selection", "Please select a vehicle from the table first.")
            return
        v = get_vehicle(vid)
        if not v:
            return

        self.selected_vehicle_id = vid
        self.vehicle_number_entry.delete(0, tk.END)
        self.vehicle_number_entry.insert(0, v["vehicle_number"])
        self.city_selector.set_value(v["city"])
        self.status_var.set(v["status"])
        self.save_btn.configure(text="Update Vehicle")

    def toggle_status(self):
        vid = self.get_selected_id()
        if not vid:
            messagebox.showwarning("No Selection", "Please select a vehicle from the table first.")
            return
        v = get_vehicle(vid)
        if not v:
            return
        new_status = "Inactive" if v["status"] == "Active" else "Active"
        if messagebox.askyesno(
            "Confirm", f"Change vehicle '{v['vehicle_number']}' status to '{new_status}'?"
        ):
            set_vehicle_status(vid, new_status)
            self.refresh_table()

    # ---------------------------------------------------------
    # SAVE / CLEAR
    # ---------------------------------------------------------
    def clear_form(self):
        self.selected_vehicle_id = None
        self.vehicle_number_entry.delete(0, tk.END)
        self.city_selector.reset()
        self.status_var.set(VEHICLE_STATUS_OPTIONS[0])
        self.save_btn.configure(text="Add Vehicle")

    def save_vehicle(self):
        vehicle_number = self.vehicle_number_entry.get().strip()
        city = self.city_selector.get_value().strip()
        status = self.status_var.get()

        if not vehicle_number:
            messagebox.showerror("Validation Error", "Vehicle number is required.")
            return
        if not city:
            messagebox.showerror("Validation Error", "Please select or type a city.")
            return

        try:
            if self.selected_vehicle_id:
                update_vehicle(self.selected_vehicle_id, vehicle_number, city, status)
                messagebox.showinfo("Success", "Vehicle updated successfully.")
            else:
                add_vehicle(vehicle_number, city, status)
                messagebox.showinfo("Success", "Vehicle added successfully.")

            self.clear_form()
            self.refresh_table()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
