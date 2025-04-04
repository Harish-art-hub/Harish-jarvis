from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()  # Load environment variables

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()
