import sqlite3
from pathlib import Path


# =====================================
# PROJECT PATH
# =====================================

PROJECT_FOLDER = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_FOLDER / "project_memory.db"


# =====================================
# DATABASE CONNECTION
# =====================================

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# =====================================
# CREATE DATABASE TABLES
# =====================================

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # =================================
    # 1. LOGIN EVENTS TABLE
    # =================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            username TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            device TEXT,
            login_attempts INTEGER,
            failed_attempts INTEGER,
            time_between_attempts REAL,
            unique_usernames INTEGER,
            ip_reputation REAL,
            rf_probability REAL,
            anomaly_score REAL,
            identity_trust REAL,
            attack_pattern_match INTEGER DEFAULT 0,
            risk_score REAL,
            status TEXT,
            attack_type TEXT,
            recommended_action TEXT,
            reason TEXT
        )
    """)

    # =================================
    # 2. IDENTITY MEMORY
    # =================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS identity_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            device TEXT NOT NULL,
            login_count INTEGER DEFAULT 0,
            suspicious_count INTEGER DEFAULT 0,
            trusted_count INTEGER DEFAULT 0,
            trust_score REAL DEFAULT 50,
            last_seen TEXT,
            last_status TEXT,
            UNIQUE(username, ip_address, device)
        )
    """)

    # =================================
    # 3. ATTACK PATTERN MEMORY
    # =================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attack_pattern_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            username TEXT,
            failed_attempts INTEGER,
            login_attempts INTEGER,
            time_between_attempts REAL,
            unique_usernames INTEGER,
            ip_reputation REAL,
            risk_score REAL,
            attack_type TEXT,
            pattern_key TEXT,
            occurrence_count INTEGER DEFAULT 1
        )
    """)

    # =================================
    # 4. DECISION RECOVERY MEMORY
    # =================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decision_recovery_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            original_decision TEXT NOT NULL,
            corrected_decision TEXT NOT NULL,
            reason TEXT,
            source_ip TEXT,
            username TEXT,
            confidence_change REAL DEFAULT 0
        )
    """)

    # =================================
    # 5. DEFENSIVE ACTIONS
    # =================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS defensive_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source_ip TEXT,
            username TEXT,
            action TEXT NOT NULL,
            action_status TEXT,
            notes TEXT
        )
    """)

    # =================================
    # 6. INVESTIGATION HISTORY
    # =================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            query TEXT NOT NULL,
            matches INTEGER DEFAULT 0,
            investigator_note TEXT
        )
    """)

    # =================================
    # 7. INDEXES
    # =================================

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_login_events_ip
        ON login_events(ip_address)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_login_events_username
        ON login_events(username)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_attack_patterns_ip
        ON attack_pattern_memory(ip_address)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_identity_username
        ON identity_memory(username)
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully.")
    print(f"Database location: {DATABASE_PATH}")


# =====================================
# RUN DIRECTLY
# =====================================

if __name__ == "__main__":
    initialize_database()

