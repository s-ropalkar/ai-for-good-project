try:
    import mysql.connector
except:
    mysql = None

import os
from dotenv import load_dotenv

load_dotenv()

def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD")
    )
