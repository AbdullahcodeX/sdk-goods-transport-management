"""
SDK GOODS - Goods Transport Management System
Main Window
--------------------------------
The root application window with a sidebar navigation menu and a
content area that swaps between screens (Vehicles, Trips, Expenses,
Diesel, Ledger, Dashboard, Monthly Report, Settings).

This is Step 3 of the build: the visual skeleton of the whole app.
Each menu button currently opens a placeholder screen. In later
steps, each placeholder will be replaced with the real, fully
working screen (forms, tables, etc.) one at a time.
"""

import tkinter as tk
from tkinter import ttk

from ui.widgets.styled_widgets import (
    COLOR_SIDEBAR_BG, COLOR_SIDEBAR_BTN, COLOR_SIDEBAR_BTN_ACTIVE,
    COLOR_SIDEBAR_TEXT, COLOR_HEADER_BG, COLOR_HEADER_TEXT,
    COLOR_CONTENT_BG, COLOR_CARD_BG, COLOR_TEXT_DARK,
    FONT_APP_TITLE, FONT_SIDEBAR_BTN, FONT_HEADER, FONT_LABEL,
)

APP_TITLE = "SDK GOODS - Transport Management System"

# Menu items: (label shown in sidebar, internal screen key)
MENU_ITEMS = [
    ("🚚  Vehicles", "vehicles"),
    ("📦  Trips", "trips"),
    ("💰  Expenses", "expenses"),
    ("⛽  Diesel", "diesel"),
    ("📒  Ledger Book", "ledger"),
    ("📊  Dashboard", "dashboard"),
    ("📅  Monthly Report", "monthly_report"),
    ("⚙️  Settings", "settings"),
]


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("1200x720")
        self.minsize(1000, 600)
        self.configure(bg=COLOR_CONTENT_BG)

        # Keep references to sidebar buttons so we can highlight the active one
        self.sidebar_buttons = {}
        self.current_screen_key = None

        self._build_sidebar()
        self._build_header()
        self._build_content_area()

        # Open the Dashboard by default when the app starts
        self.show_screen("dashboard")

    # ---------------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------------
    def _build_sidebar(self):
        sidebar = tk.Frame(self, bg=COLOR_SIDEBAR_BG, width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Company / App branding at the top of the sidebar
        brand_frame = tk.Frame(sidebar, bg=COLOR_SIDEBAR_BG, height=90)
        brand_frame.pack(fill="x", pady=(15, 10))
        tk.Label(
            brand_frame, text="SDK GOODS", bg=COLOR_SIDEBAR_BG,
            fg=COLOR_SIDEBAR_TEXT, font=FONT_APP_TITLE
        ).pack()
        tk.Label(
            brand_frame, text="Transport Management", bg=COLOR_SIDEBAR_BG,
            fg="#9CA3AF", font=FONT_LABEL
        ).pack()

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=15, pady=(0, 10))

        # Navigation buttons
        for label, key in MENU_ITEMS:
            btn = tk.Button(
                sidebar, text=label, anchor="w", bg=COLOR_SIDEBAR_BTN,
                fg=COLOR_SIDEBAR_TEXT, font=FONT_SIDEBAR_BTN, bd=0,
                activebackground=COLOR_SIDEBAR_BTN_ACTIVE,
                activeforeground=COLOR_SIDEBAR_TEXT,
                relief="flat", padx=20, pady=12, cursor="hand2",
                command=lambda k=key: self.show_screen(k)
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.sidebar_buttons[key] = btn

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------
    def _build_header(self):
        self.header = tk.Frame(self, bg=COLOR_HEADER_BG, height=60)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        self.header_label = tk.Label(
            self.header, text="Dashboard", bg=COLOR_HEADER_BG,
            fg=COLOR_HEADER_TEXT, font=FONT_HEADER
        )
        self.header_label.pack(side="left", padx=25)

    # ---------------------------------------------------------
    # CONTENT AREA
    # ---------------------------------------------------------
    def _build_content_area(self):
        self.content_area = tk.Frame(self, bg=COLOR_CONTENT_BG)
        self.content_area.pack(side="top", fill="both", expand=True)

    def _clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------
    # SCREEN SWITCHING
    # ---------------------------------------------------------
    def show_screen(self, key):
        """Switches the visible screen and highlights the active sidebar button."""
        self.current_screen_key = key
        self._clear_content_area()

        # Highlight active button, reset others
        for k, btn in self.sidebar_buttons.items():
            btn.configure(bg=COLOR_SIDEBAR_BTN_ACTIVE if k == key else COLOR_SIDEBAR_BTN)

        # Update header title
        titles = {
            "vehicles": "Vehicles",
            "trips": "Trips",
            "expenses": "Expenses",
            "diesel": "Diesel",
            "ledger": "Ledger Book",
            "dashboard": "Dashboard",
            "monthly_report": "Monthly Report",
            "settings": "Settings",
        }
        self.header_label.configure(text=titles.get(key, key.title()))

        screen_classes = {
            "vehicles": ("ui.vehicle_screen", "VehicleScreen"),
            "trips": ("ui.trip_screen", "TripScreen"),
            "expenses": ("ui.expense_screen", "ExpenseScreen"),
            "diesel": ("ui.diesel_screen", "DieselScreen"),
            "ledger": ("ui.ledger_screen", "LedgerScreen"),
            "dashboard": ("ui.dashboard_screen", "DashboardScreen"),
            "monthly_report": ("ui.monthly_report_screen", "MonthlyReportScreen"),
            "settings": ("ui.settings_screen", "SettingsScreen"),
        }

        if key in screen_classes:
            module_name, class_name = screen_classes[key]
            import importlib
            module = importlib.import_module(module_name)
            screen_class = getattr(module, class_name)
            screen = screen_class(self.content_area)
            screen.pack(fill="both", expand=True)
        else:
            self._render_placeholder_screen(key, titles.get(key, key.title()))

    def _render_placeholder_screen(self, key, title):
        """
        Temporary placeholder screen shown until each module is built
        in its own step. Replaced one-by-one with real functionality.
        """
        card = tk.Frame(self.content_area, bg=COLOR_CARD_BG, bd=0)
        card.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            card, text=f"{title} screen", bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_DARK, font=FONT_APP_TITLE
        ).pack(pady=(40, 10))

        tk.Label(
            card,
            text=f"This section ('{key}') will be built in the next development step.",
            bg=COLOR_CARD_BG, fg="#6B7280", font=FONT_LABEL
        ).pack()


def run_app():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    run_app()
