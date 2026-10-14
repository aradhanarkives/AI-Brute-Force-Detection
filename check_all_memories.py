import sqlite3
from pathlib import Path


project_folder = Path(__file__).resolve().parent
database_path = project_folder / "project_memory.db"


connection = sqlite3.connect(database_path)
cursor = connection.cursor()


# Check Identity Stability Memory
cursor.execute("SELECT COUNT(*) FROM identity_memory")
identity_count = cursor.fetchone()[0]


# Check Attack Pattern Memory
cursor.execute("SELECT COUNT(*) FROM attack_pattern_memory")
attack_count = cursor.fetchone()[0]


# Check Decision Recovery Memory
cursor.execute("SELECT COUNT(*) FROM decision_recovery_memory")
recovery_count = cursor.fetchone()[0]


connection.close()


print("THREE-MEMORY SYSTEM STATUS")
print("--------------------------")
print("Identity Memory Records:", identity_count)
print("Attack Pattern Records:", attack_count)
print("Decision Recovery Records:", recovery_count)

if identity_count > 0 and attack_count > 0 and recovery_count > 0:
    print("Status: ALL THREE MEMORIES ARE ACTIVE")
else:
    print("Status: SOME MEMORY RECORDS ARE MISSING")