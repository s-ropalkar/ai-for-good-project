import pandas as pd
import numpy as np

np.random.seed(42)

# Parameters
num_days = 10
locations = ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"]

products = [
    ("P001", "Rice Pack", "Food"),
    ("P002", "Wheat Flour", "Food"),
    ("P003", "Biscuits", "Food"),
    ("P004", "Milk Powder", "Food"),
    ("P005", "Paracetamol", "Medicine"),
    ("P006", "ORS Packets", "Medicine"),
    ("P007", "Sanitizer", "Hygiene"),
    ("P008", "Soap", "Hygiene"),
]

dates = pd.date_range(start="2025-01-01", periods=num_days)

rows = []

for date in dates:
    for location in locations:
        for pid, pname, category in products:
            opening_stock = np.random.randint(50, 400)
            received = np.random.randint(0, 100)
            issued = np.random.randint(10, 80)

            closing_stock = max(opening_stock + received - issued, 0)

            daily_sales_avg = np.random.randint(5, 60)
            days_to_expiry = np.random.randint(1, 15)
            lead_time_days = np.random.randint(2, 7)

            rows.append([
                date,
                location,
                pid,
                pname,
                category,
                opening_stock,
                received,
                issued,
                closing_stock,
                daily_sales_avg,
                days_to_expiry,
                lead_time_days
            ])

# Create DataFrame
inventory_df = pd.DataFrame(rows, columns=[
    "date",
    "location",
    "product_id",
    "product_name",
    "category",
    "opening_stock",
    "received",
    "issued",
    "closing_stock",
    "daily_sales_avg",
    "days_to_expiry",
    "lead_time_days"
])

# Limit to ~100 rows
inventory_df = inventory_df.sample(100, random_state=42)

# Save CSV
inventory_df.to_csv("inventory_data.csv", index=False)

print("✅ inventory_data.csv created with", len(inventory_df), "rows")
