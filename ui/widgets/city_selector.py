"""
SDK GOODS - Goods Transport Management System
City Selector Widget
--------------------------------
A reusable dropdown for picking a Pakistani city, with an
automatic manual-entry box that appears when "Other" is selected.

Used in: Vehicle screen (base city) and Trip screen (from/to city).
"""

import tkinter as tk
from tkinter import ttk

from utils.constants import PAKISTANI_CITIES, OTHER_OPTION


class CitySelector(tk.Frame):
    def __init__(self, parent, initial_city=None, width=27, **kwargs):
        super().__init__(parent, **kwargs)

        bg = kwargs.get("bg", None)

        self.combo_var = tk.StringVar()
        self.other_var = tk.StringVar()

        self.combo = ttk.Combobox(
            self, textvariable=self.combo_var, values=PAKISTANI_CITIES,
            state="readonly", width=width
        )
        self.combo.grid(row=0, column=0, sticky="w")
        self.combo.bind("<<ComboboxSelected>>", self._on_select)

        self.other_entry = tk.Entry(self, textvariable=self.other_var, width=width + 2)
        # not shown until "Other" is chosen

        if initial_city:
            self.set_value(initial_city)
        else:
            self.combo_var.set(PAKISTANI_CITIES[0])

    def _on_select(self, event=None):
        if self.combo_var.get() == OTHER_OPTION:
            self.other_entry.grid(row=1, column=0, sticky="w", pady=(5, 0))
            self.other_entry.focus_set()
        else:
            self.other_entry.grid_forget()
            self.other_var.set("")

    def get_value(self):
        """Returns the final selected/typed city name as plain text."""
        if self.combo_var.get() == OTHER_OPTION:
            return self.other_var.get().strip()
        return self.combo_var.get()

    def set_value(self, city):
        """Pre-fills the widget with an existing city value (used when editing)."""
        if city in PAKISTANI_CITIES:
            self.combo_var.set(city)
            self.other_entry.grid_forget()
            self.other_var.set("")
        else:
            self.combo_var.set(OTHER_OPTION)
            self.other_var.set(city)
            self.other_entry.grid(row=1, column=0, sticky="w", pady=(5, 0))

    def reset(self):
        self.combo_var.set(PAKISTANI_CITIES[0])
        self.other_entry.grid_forget()
        self.other_var.set("")
