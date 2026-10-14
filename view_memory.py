import sqlite3
from pathlib import Path


project_folder = Path(__file__).resolve().parent
database_path = project_folder / "project_memory.db"


connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("""
    SELECT username, ip_address, device, login_count, suspicious_count
    FROM identity_memory
""")

records = cursor.fetchall()

print("IDENTITY STABILITY MEMORY")
print("-------------------------")

for record in records:
    print("Username:", record[0])
    print("IP Address:", record[1])
    print("Device:", record[2])
    print("Login Count:", record[3])
    print("Suspicious Count:", record[4])
    print("-------------------------")

connection.close()