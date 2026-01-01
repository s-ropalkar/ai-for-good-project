import pandas as pd
import os
from mysql_connector import get_mysql_connection


conn = get_mysql_connection()
cursor = conn.cursor()

# ---------- CREATE DATABASE ----------
cursor.execute("CREATE DATABASE IF NOT EXISTS smart_distribution")
cursor.execute("USE smart_distribution")

# ---------- INVENTORY TABLE ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    date DATE,
    location VARCHAR(50),
    product_id VARCHAR(20),
    product_name VARCHAR(100),
    category VARCHAR(50),
    opening_stock INT,
    received INT,
    issued INT,
    closing_stock INT,
    daily_sales_avg FLOAT,
    days_to_expiry INT,
    lead_time_days INT,
    PRIMARY KEY (date, location, product_id)
)
""")

# ---------- NGO TABLE ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS ngo_master (
    ngo_id VARCHAR(20) PRIMARY KEY,
    ngo_name VARCHAR(100),
    location VARCHAR(50),
    category_accepted VARCHAR(50),
    min_shelf_life_days INT,
    daily_capacity_units INT,
    contact_email VARCHAR(100),
    active_flag BOOLEAN
)
""")

# ---------- LOAD INVENTORY CSV ----------


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

inventory_path = os.path.join(BASE_DIR, "inventory_data.csv")
ngo_path = os.path.join(BASE_DIR, "ngo_master.csv")

print("Inventory CSV Path:", inventory_path)
print("Exists:", os.path.exists(inventory_path))
inventory_df = pd.read_csv(inventory_path)

for _, row in inventory_df.iterrows():
    cursor.execute("""
        INSERT INTO inventory VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(row))

# ---------- LOAD NGO CSV ----------
ngo_df = pd.read_csv(ngo_path)

# Convert Y/N → 1/0
ngo_df["active_flag"] = ngo_df["active_flag"].map({"Y": 1, "N": 0})

for _, row in ngo_df.iterrows():
    cursor.execute("""
        INSERT INTO ngo_master VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(row))


conn.commit()
conn.close()

print("MySQL tables created and CSV data loaded successfully")
