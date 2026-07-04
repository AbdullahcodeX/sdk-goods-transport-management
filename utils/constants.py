"""
SDK GOODS - Goods Transport Management System
Constants
--------------------------------
Central place for all dropdown lists used across the app.
Change a list here and it updates everywhere automatically.
"""

# Special value used whenever a dropdown needs a manual/custom entry
OTHER_OPTION = "Other (Type manually)"

# ---------------------------------------------------------
# MAJOR PAKISTANI CITIES (for vehicle base city + trip from/to city)
# ---------------------------------------------------------
PAKISTANI_CITIES = [
    "Karachi",
    "Lahore",
    "Islamabad",
    "Rawalpindi",
    "Faisalabad",
    "Multan",
    "Peshawar",
    "Quetta",
    "Sialkot",
    "Gujranwala",
    "Hyderabad",
    "Sukkur",
    "Bahawalpur",
    "Sargodha",
    "Sahiwal",
    "Rahim Yar Khan",
    "Gujrat",
    "Sheikhupura",
    "Jhang",
    "Dera Ghazi Khan",
    "Larkana",
    "Mardan",
    "Abbottabad",
    "Mirpur (AJK)",
    "Muzaffarabad",
    "Gwadar",
    "Vehari",
    "Okara",
    "Kasur",
    "Chiniot",
    OTHER_OPTION,  # always keep this LAST in the list
]

# ---------------------------------------------------------
# VEHICLE STATUS OPTIONS
# ---------------------------------------------------------
VEHICLE_STATUS_OPTIONS = ["Active", "In Workshop", "Inactive"]

# ---------------------------------------------------------
# WEIGHT UNITS
# ---------------------------------------------------------
WEIGHT_UNITS = ["Tons", "Mann"]

# ---------------------------------------------------------
# DIESEL TYPES
# ---------------------------------------------------------
DIESEL_TYPES = ["Irani (Iranian)", "Pakistani", "Other"]

# ---------------------------------------------------------
# EXPENSE CATEGORIES - split into Fixed and Other
# (Used in the Expense screen, grouped under "Fixed Expense" / "Other Expense")
# ---------------------------------------------------------
FIXED_EXPENSE_CATEGORIES = [
    "Tools",          # as requested: tools/tolls type routine costs
    "Food Expense",
    "Tyre Expense",
    "Police Expense",
]

OTHER_EXPENSE_CATEGORIES = [
    "Inaam (Goods Bonus/Reward)",
    "Motorway Toll Plaza",
    "GT Road Toll Plaza",
    "Vehicle Work Cost",
    "Other Expense",
]

# Combined list (useful for reports/filters showing all categories together)
ALL_EXPENSE_CATEGORIES = FIXED_EXPENSE_CATEGORIES + OTHER_EXPENSE_CATEGORIES

# ---------------------------------------------------------
# EXPENSE GROUPS
# ---------------------------------------------------------
EXPENSE_GROUPS = ["Fixed", "Other"]


if __name__ == "__main__":
    # Quick self-test: print every list so you can visually confirm it's correct
    print("PAKISTANI CITIES:", len(PAKISTANI_CITIES), "options")
    for c in PAKISTANI_CITIES:
        print("   -", c)

    print("\nVEHICLE STATUS OPTIONS:", VEHICLE_STATUS_OPTIONS)
    print("WEIGHT UNITS:", WEIGHT_UNITS)
    print("DIESEL TYPES:", DIESEL_TYPES)
    print("\nFIXED EXPENSE CATEGORIES:", FIXED_EXPENSE_CATEGORIES)
    print("OTHER EXPENSE CATEGORIES:", OTHER_EXPENSE_CATEGORIES)
