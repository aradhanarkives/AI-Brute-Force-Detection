import sqlite3
from pathlib import Path

project_folder = Path(__file__).resolve().parent
database_path = project_folder / "project_memory.db"

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(identity_memory)")

columns = cursor.fetchall()

print("Columns in identity_memory table:")

for column in columns:
    print(column)

connection.close()