"""
SDK GOODS - Goods Transport Management System
Settings Screen
--------------------------------
Edit company information (name, owner, address, phone).
This info can later be used on printed reports/receipts.
"""

import tkinter as tk
from tkinter import messagebox

from models.settings_model import get_settings, update_settings
from ui.widgets.styled_widgets import (
    COLOR_CONTENT_BG, COLOR_CARD_BG, COLOR_TEXT_DARK, COLOR_HEADER_BG,
    FONT_HEADER, FONT_LABEL, FONT_LABEL_BOLD,
)


class SettingsScreen(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_CONTENT_BG, **kwargs)
        self._build_form()
        self.load_settings()

    def _build_form(self):
        card = tk.Frame(self, bg=COLOR_CARD_BG)
        card.pack(fill="x", padx=25, pady=25)

        tk.Label(
            card, text="Company Settings", font=FONT_HEADER, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 15))

        tk.Label(card, text="Company Name:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=1, column=0, sticky="w", padx=20, pady=8)
        self.company_name_entry = tk.Entry(card, font=FONT_LABEL, width=40)
        self.company_name_entry.grid(row=1, column=1, sticky="w", pady=8)

        tk.Label(card, text="Owner Name:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=2, column=0, sticky="w", padx=20, pady=8)
        self.owner_name_entry = tk.Entry(card, font=FONT_LABEL, width=40)
        self.owner_name_entry.grid(row=2, column=1, sticky="w", pady=8)

        tk.Label(card, text="Address:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=3, column=0, sticky="w", padx=20, pady=8)
        self.address_entry = tk.Entry(card, font=FONT_LABEL, width=40)
        self.address_entry.grid(row=3, column=1, sticky="w", pady=8)

        tk.Label(card, text="Phone:", font=FONT_LABEL_BOLD, bg=COLOR_CARD_BG)\
            .grid(row=4, column=0, sticky="w", padx=20, pady=8)
        self.phone_entry = tk.Entry(card, font=FONT_LABEL, width=40)
        self.phone_entry.grid(row=4, column=1, sticky="w", pady=8)

        tk.Button(
            card, text="Save Settings", bg=COLOR_HEADER_BG, fg="white", font=FONT_LABEL_BOLD,
            padx=16, pady=7, bd=0, cursor="hand2", command=self.save_settings
        ).grid(row=5, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 20))

    def load_settings(self):
        s = get_settings()
        if not s:
            return
        self.company_name_entry.insert(0, s["company_name"] or "")
        self.owner_name_entry.insert(0, s["owner_name"] or "")
        self.address_entry.insert(0, s["address"] or "")
        self.phone_entry.insert(0, s["phone"] or "")

    def save_settings(self):
        company_name = self.company_name_entry.get().strip()
        if not company_name:
            messagebox.showerror("Validation Error", "Company name is required.")
            return

        update_settings(
            company_name=company_name,
            owner_name=self.owner_name_entry.get().strip(),
            address=self.address_entry.get().strip(),
            phone=self.phone_entry.get().strip(),
        )
        messagebox.showinfo("Success", "Settings saved successfully.")
