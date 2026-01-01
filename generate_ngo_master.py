import pandas as pd

ngo_data = [
    ["NGO01", "FoodCare Trust", "Mumbai", "Food", 1, 300, "foodcare@ngo.org", "Y"],
    ["NGO02", "HealthFirst NGO", "Pune", "Medicine", 3, 150, "healthfirst@ngo.org", "Y"],
    ["NGO03", "Community Aid", "Nagpur", "Food", 2, 200, "community@ngo.org", "Y"],
    ["NGO04", "Helping Hands", "Nashik", "Hygiene", 2, 180, "helpinghands@ngo.org", "Y"],
    ["NGO05", "Relief Network", "Aurangabad", "Food", 1, 250, "relief@ngo.org", "Y"],
    ["NGO06", "MedSupport", "Mumbai", "Medicine", 4, 120, "medsupport@ngo.org", "Y"]
]

ngo_df = pd.DataFrame(ngo_data, columns=[
    "ngo_id",
    "ngo_name",
    "location",
    "category_accepted",
    "min_shelf_life_days",
    "daily_capacity_units",
    "contact_email",
    "active_flag"
])

ngo_df.to_csv("ngo_master.csv", index=False)

print("✅ ngo_master.csv created with", len(ngo_df), "rows")
