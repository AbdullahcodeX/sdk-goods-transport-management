"""
SDK GOODS - Goods Transport Management System
Main Entry Point
--------------------------------
Run this file to start the application:
    python3 main.py

On first run, it will automatically create the SQLite database
and all required tables (in Documents/SDK_GOODS_TransportApp/).
"""

from database.db_manager import initialize_database
from ui.main_window import run_app

if __name__ == "__main__":
    # Step 1: Make sure the database and tables exist
    initialize_database()

    # Step 2: Launch the Tkinter application
    run_app()
