import pandas as pd
import mysql.connector
from datetime import date

# ---------- DB CONNECTION ----------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Wsrsid@75",
    database="smart_distribution"
)

cursor = conn.cursor()

# ---------- LOAD INVENTORY ----------
inventory = pd.read_sql("SELECT * FROM inventory", conn)

# ---------- SAFE METRICS ----------
inventory["demand_score"] = inventory.apply(
    lambda x: x["daily_sales_avg"] / x["closing_stock"]
    if x["closing_stock"] > 0 else 0,
    axis=1
)

inventory["stockout_days"] = inventory.apply(
    lambda x: x["closing_stock"] / x["daily_sales_avg"]
    if x["daily_sales_avg"] > 0 else 999,
    axis=1
)

# ---------- DECISION RULE ----------
def decide(row):
    if row["days_to_expiry"] <= 3 and row["demand_score"] < 0.3:
        return "DONATE", "Near expiry & low demand"
    elif row["stockout_days"] <= row["lead_time_days"]:
        return "REORDER", "Stock may run out before replenishment"
    else:
        return "OK", "Healthy stock"

# Apply decision
inventory[["decision", "decision_reason"]] = inventory.apply(
    lambda r: pd.Series(decide(r)),
    axis=1
)


# ---------- UPDATE MYSQL ----------
for _, row in inventory.iterrows():
    cursor.execute("""
        UPDATE inventory
        SET decision = %s,
            decision_reason = %s
            
        WHERE `date` = %s
          AND location = %s
          AND product_id = %s
    """, (
        row["decision"],
        row["decision_reason"],
        row["date"],
        row["location"],
        row["product_id"]
    ))

conn.commit()
conn.close()

print("✅ Analytics & decisions stored directly in MySQL")
