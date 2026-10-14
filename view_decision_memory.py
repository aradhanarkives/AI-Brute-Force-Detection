import sqlite3
from pathlib import Path


project_folder = Path(__file__).resolve().parent
database_path = project_folder / "project_memory.db"


connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("""
    SELECT
        original_decision,
        corrected_decision,
        reason
    FROM decision_recovery_memory
""")

records = cursor.fetchall()

print("DECISION RECOVERY MEMORY")
print("------------------------")

for record in records:
    print("Original Decision:", record[0])
    print("Corrected Decision:", record[1])
    print("Reason:", record[2])
    print("------------------------")

connection.close()