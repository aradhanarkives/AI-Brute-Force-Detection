import sqlite3
from pathlib import Path


project_folder = Path(__file__).resolve().parent
database_path = project_folder / "project_memory.db"


connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("""
    SELECT
        ip_address,
        failed_attempts,
        login_attempts,
        time_between_attempts,
        unique_usernames,
        ip_reputation,
        risk_score
    FROM attack_pattern_memory
""")

records = cursor.fetchall()

print("ATTACK PATTERN MEMORY")
print("---------------------")

for record in records:
    print("IP Address:", record[0])
    print("Failed Attempts:", record[1])
    print("Login Attempts:", record[2])
    print("Time Between Attempts:", record[3])
    print("Unique Usernames:", record[4])
    print("IP Reputation:", record[5])
    print("Risk Score:", record[6])
    print("---------------------")

connection.close()