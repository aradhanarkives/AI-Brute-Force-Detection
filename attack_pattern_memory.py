import sqlite3
from pathlib import Path
from datetime import datetime


# ==========================================
# DATABASE PATH
# ==========================================

project_folder = Path(__file__).resolve().parent
database_path = project_folder / "project_memory.db"


# ==========================================
# SAVE ATTACK PATTERN
# ==========================================

def save_attack_pattern(
    ip_address,
    failed_attempts,
    login_attempts,
    time_between_attempts,
    unique_usernames,
    ip_reputation,
    risk_score,
    username="unknown",
    attack_type="Brute Force",
    pattern_key=None
):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Automatically create a pattern key if not provided
    if pattern_key is None:
        pattern_key = (
            f"{ip_address}_"
            f"{failed_attempts}_"
            f"{login_attempts}_"
            f"{unique_usernames}"
        )

    # Check whether this pattern already exists
    cursor.execute("""
        SELECT id, occurrence_count
        FROM attack_pattern_memory
        WHERE pattern_key = ?
    """, (pattern_key,))

    existing_pattern = cursor.fetchone()

    if existing_pattern:
        pattern_id = existing_pattern[0]
        old_count = existing_pattern[1]

        cursor.execute("""
            UPDATE attack_pattern_memory
            SET
                timestamp = ?,
                ip_address = ?,
                username = ?,
                failed_attempts = ?,
                login_attempts = ?,
                time_between_attempts = ?,
                unique_usernames = ?,
                ip_reputation = ?,
                risk_score = ?,
                attack_type = ?,
                occurrence_count = ?
            WHERE id = ?
        """, (
            timestamp,
            ip_address,
            username,
            failed_attempts,
            login_attempts,
            time_between_attempts,
            unique_usernames,
            ip_reputation,
            risk_score,
            attack_type,
            old_count + 1,
            pattern_id
        ))

        print("Existing attack pattern updated successfully!")

    else:
        cursor.execute("""
            INSERT INTO attack_pattern_memory
            (
                timestamp,
                ip_address,
                username,
                failed_attempts,
                login_attempts,
                time_between_attempts,
                unique_usernames,
                ip_reputation,
                risk_score,
                attack_type,
                pattern_key,
                occurrence_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            ip_address,
            username,
            failed_attempts,
            login_attempts,
            time_between_attempts,
            unique_usernames,
            ip_reputation,
            risk_score,
            attack_type,
            pattern_key,
            1
        ))

        print("New attack pattern saved successfully!")

    connection.commit()
    connection.close()


# ==========================================
# GET SIMILAR ATTACK PATTERN
# ==========================================

def get_similar_attack_pattern(
    ip_address,
    failed_attempts,
    login_attempts,
    unique_usernames
):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM attack_pattern_memory
        WHERE
            ip_address = ?
            OR (
                failed_attempts = ?
                AND login_attempts = ?
                AND unique_usernames = ?
            )
        ORDER BY occurrence_count DESC
        LIMIT 1
    """, (
        ip_address,
        failed_attempts,
        login_attempts,
        unique_usernames
    ))

    pattern = cursor.fetchone()
    connection.close()

    return pattern


# ==========================================
# TEST ATTACK PATTERN MEMORY
# ==========================================

if __name__ == "__main__":

    save_attack_pattern(
        ip_address="192.168.1.10",
        failed_attempts=8,
        login_attempts=10,
        time_between_attempts=1.5,
        unique_usernames=4,
        ip_reputation=0.2,
        risk_score=78.5,
        username="aradhana",
        attack_type="Brute Force"
    )

    pattern = get_similar_attack_pattern(
        ip_address="192.168.1.10",
        failed_attempts=8,
        login_attempts=10,
        unique_usernames=4
    )

    if pattern:
        print("\nSimilar Attack Pattern Found:")
        print("IP Address:", pattern["ip_address"])
        print("Username:", pattern["username"])
        print("Risk Score:", pattern["risk_score"])
        print("Attack Type:", pattern["attack_type"])
        print("Occurrences:", pattern["occurrence_count"])
    else:
        print("\nNo similar attack pattern found.")