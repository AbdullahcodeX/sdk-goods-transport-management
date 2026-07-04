# SDK GOODS — Transport Management System

A complete, professional desktop application to manage a fleet of goods
transport vehicles: vehicles, trips, expenses, diesel, a full ledger book,
a dashboard, and monthly reports. Built with **Python + Tkinter + SQLite**.
No login system.

---

## ✅ Everything included in this version (fully working)

| Screen | What it does |
|---|---|
| **Vehicles** | Add/edit your 15+ vehicles, pick a city (30+ Pakistani cities + "Other" manual entry), Activate/Deactivate, search |
| **Trips** | Full trip form per vehicle: date, from/to city, goods/maal, weight, broker, station, total brokery, wasool kiraya, **auto-calculated remaining kiraya**, daily wages, notes. Edit & delete trips |
| **Expenses** | Fixed (Tools, Food, Tyre, Police) and Other (Inaam, Motorway Toll, GT Road Toll, Vehicle Work Cost, Other) expenses per trip, with running total |
| **Diesel** | Irani / Pakistani / Other diesel entries per trip with auto-calculated total cost (liters × rate) |
| **Ledger Book** | Full itemized statement per trip: trip info + all expenses + all diesel + final Total Cost and Net Saving/Loss |
| **Dashboard** | Company-wide totals (all vehicles) + per-vehicle summary table + trip-by-trip breakdown (double-click a vehicle row) |
| **Monthly Report** | Pick a vehicle + a month → see that month's total income, expense, and net saving, plus the list of trips |
| **Settings** | Company name (pre-filled with **SDK GOODS**), owner, address, phone |

All financial numbers (Remaining Kiraya, Total Expense, Net Saving) are
**calculated automatically** by the app — you never need to do the math
yourself, and the Ledger, Dashboard, and Monthly Report always agree with
each other because they all use the same calculation logic
(`utils/calculations.py`).

---

## 📂 Folder Structure

```
GoodsTransportApp/
├── main.py                        # Run this to start the app
├── requirements.txt
├── database/
│   └── db_manager.py               # Creates the SQLite database + all tables
├── models/                         # All database read/write logic
│   ├── vehicle_model.py
│   ├── trip_model.py
│   ├── expense_model.py
│   ├── diesel_model.py
│   └── settings_model.py
├── ui/                              # All screens (Tkinter)
│   ├── main_window.py               # Sidebar + screen switching
│   ├── vehicle_screen.py
│   ├── trip_screen.py
│   ├── expense_screen.py
│   ├── diesel_screen.py
│   ├── ledger_screen.py
│   ├── dashboard_screen.py
│   ├── monthly_report_screen.py
│   ├── settings_screen.py
│   └── widgets/
│       ├── city_selector.py         # Reusable city dropdown + "Other"
│       └── styled_widgets.py        # Shared colors/fonts (theme)
├── utils/
│   ├── constants.py                 # Cities, diesel types, expense categories
│   └── calculations.py              # All money-math formulas in one place
└── assets/                          # (for logo/icons later)
```

---

## ▶️ HOW TO RUN (Ubuntu)

```bash
# 1) Unzip the project
unzip SDK_GOODS_App.zip
cd GoodsTransportApp

# 2) Install tkinter (Ubuntu does not include it by default)
sudo apt update
sudo apt install python3-tk -y

# 3) (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 4) Install Python dependencies (used for later export/build features)
pip install -r requirements.txt

# 5) Run the app
python3 main.py
```

On first run, the app automatically creates its database at:
```
~/Documents/SDK_GOODS_TransportApp/transport.db
```
This file holds ALL your data permanently (vehicles, trips, expenses, diesel,
settings). Back it up regularly (see "Backing up your data" below).

---

## 🧭 Suggested first-time workflow

1. Open the app → go to **Settings** → confirm/update your company details → Save
2. Go to **Vehicles** → add all 15+ of your vehicles (vehicle number + city)
3. Go to **Trips** → select a vehicle → add a trip with all details
4. Go to **Expenses** → select the same vehicle & trip → add each expense
5. Go to **Diesel** → select the same vehicle & trip → add diesel purchases
6. Go to **Ledger Book** → select the vehicle & trip → see the full statement
   with the final Net Saving
7. Go to **Dashboard** → see company-wide totals and every vehicle's savings
8. Go to **Monthly Report** → pick a vehicle and a month to see that month's totals

---

## 💾 Backing up your data

Your entire database is one file:
```
~/Documents/SDK_GOODS_TransportApp/transport.db
```
Copy this file anywhere (USB drive, cloud folder, email to yourself) to back
it up. To restore, simply put a backed-up copy back in that same folder.

---

## 🏗️ Building a Windows/Linux .exe / standalone executable for your client

This app is pure Python + Tkinter + SQLite, so it can be packaged with
**PyInstaller** into a single executable your client can double-click —
no Python installation needed on their machine.

```bash
# Run this from inside the GoodsTransportApp folder (with venv activated)
pip install pyinstaller
pyinstaller --onefile --windowed --name "SDK_GOODS_Transport" main.py
```

- The finished executable will appear in the `dist/` folder.
- `--windowed` hides the console/terminal window (professional look).
- To build a **Windows .exe specifically**, this command must be run
  **on a Windows machine** (PyInstaller builds for the OS it runs on —
  it cannot cross-compile from Ubuntu to Windows .exe). If your client uses
  Windows, either:
  - Run this same command on a Windows PC (with Python installed), or
  - Ask me and we'll set up a Windows build step next.
- On Ubuntu, this command produces a Linux executable your client can run
  the same way if they also use Ubuntu/Linux.

This is the **final step** of the whole project — we'll do it once every
screen above has been tested and confirmed working on your machine.

---

## 🔜 Not included yet (planned next, on request)
- Export any report to Excel/PDF
- One-click backup/restore button inside the app
- Printable trip receipt
- Charts on the dashboard (bar/line graphs)
- Company logo on Settings/printed reports

Tell me which of these you'd like next, or if you're ready to move to the
final `.exe` packaging step.
