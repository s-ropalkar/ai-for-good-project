import pandas as pd
import mysql.connector
from snowflake_connector import get_snowflake_connection

# ---------- MYSQL ----------
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Wsrsid@75",
    database="smart_distribution"
)

query = """
SELECT
    product_id,
    product_name,
    category,
    location,
    decision,
    decision_reason
FROM inventory
"""

df = pd.read_sql(query, mysql_conn)
mysql_conn.close()

# ---------- SNOWFLAKE ----------
sf_conn = get_snowflake_connection()
cs = sf_conn.cursor()

cs.execute("USE DATABASE SMART_DONATION_DB")
cs.execute("USE SCHEMA PUBLIC")


cs.execute("""
CREATE TABLE IF NOT EXISTS INVENTORY_DECISIONS (
    product_id STRING,
    product_name STRING,
    category STRING,
    location STRING,
    decision STRING,
    decision_reason STRING
)
""")

# Insert data
for _, row in df.iterrows():
    cs.execute("""
        INSERT INTO INVENTORY_DECISIONS
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))

sf_conn.commit()
cs.close()
sf_conn.close()

print("✅ Data loaded into Snowflake successfully")
