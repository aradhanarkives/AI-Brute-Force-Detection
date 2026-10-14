import sqlite3
from pathlib import Path


# Find the main project folder
project_folder = Path(__file__).resolve().parent

# Database file
database_path = project_folder / "project_memory.db"


# Connect to database
connection = sqlite3.connect(database_path)
cursor = connection.cursor()


# Memory 1: Identity Stability Memory
cursor.execute("""
    CREATE TABLE IF NOT EXISTS identity_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        ip_address TEXT,
        device TEXT,
        login_count INTEGER DEFAULT 0,
        suspicious_count INTEGER DEFAULT 0
    )
""")


# Memory 2: Attack Pattern Memory
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attack_pattern_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT,
        failed_attempts INTEGER,
        login_attempts INTEGER,
        time_between_attempts REAL,
        unique_usernames INTEGER,
        ip_reputation REAL,
        risk_score REAL
    )
""")


# Memory 3: Decision Recovery Memory
cursor.execute("""
    CREATE TABLE IF NOT EXISTS decision_recovery_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_decision TEXT,
        corrected_decision TEXT,
        reason TEXT
    )
""")


connection.commit()
connection.close()


print("Three-memory database created successfully!")
print("Database location:")
print(database_path)