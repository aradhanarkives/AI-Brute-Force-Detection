import sqlite3
from pathlib import Path
from datetime import datetime


# =====================================
# DATABASE PATH
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
# GET IDENTITY INFORMATION
# =====================================

def get_identity(username, ip_address, device):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM identity_memory
        WHERE username = ?
        AND ip_address = ?
        AND device = ?
    """, (
        username,
        ip_address,
        device
    ))

    record = cursor.fetchone()
    connection.close()

    return record


# =====================================
# CALCULATE IDENTITY TRUST
# =====================================

def calculate_identity_trust(record):

    if record is None:
        return 50.0

    login_count = record["login_count"]
    suspicious_count = record["suspicious_count"]
    trusted_count = record["trusted_count"]

    total_events = login_count

    if total_events == 0:
        return 50.0

    suspicious_rate = suspicious_count / total_events
    trusted_rate = trusted_count / total_events

    trust_score = 50

    trust_score += trusted_rate * 40
    trust_score -= suspicious_rate * 50

    trust_score = max(0, min(100, trust_score))

    return round(trust_score, 2)


# =====================================
# GET IDENTITY STATUS
# =====================================

def get_identity_status(
    username,
    ip_address,
    device
):

    record = get_identity(
        username,
        ip_address,
        device
    )

    if record is None:
        return "NEW IDENTITY"

    trust_score = calculate_identity_trust(record)

    if trust_score >= 75:
        return "TRUSTED IDENTITY"

    if trust_score <= 30:
        return "HIGH RISK IDENTITY"

    return "SUSPICIOUS IDENTITY"


# =====================================
# UPDATE IDENTITY MEMORY
# =====================================

def update_identity_memory(
    username,
    ip_address,
    device,
    decision
):

    connection = get_connection()
    cursor = connection.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    suspicious_value = (
        1 if decision in ["HIGH RISK", "MEDIUM RISK"]
        else 0
    )

    trusted_value = (
        1 if decision == "LOW RISK"
        else 0
    )

    existing_record = get_identity(
        username,
        ip_address,
        device
    )

    if existing_record is None:

        initial_trust = 30 if suspicious_value else 70

        cursor.execute("""
            INSERT INTO identity_memory
            (
                username,
                ip_address,
                device,
                login_count,
                suspicious_count,
                trusted_count,
                trust_score,
                last_seen,
                last_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            ip_address,
            device,
            1,
            suspicious_value,
            trusted_value,
            initial_trust,
            timestamp,
            decision
        ))

    else:

        login_count = existing_record["login_count"] + 1
        suspicious_count = (
            existing_record["suspicious_count"]
            + suspicious_value
        )
        trusted_count = (
            existing_record["trusted_count"]
            + trusted_value
        )

        total_events = login_count

        suspicious_rate = suspicious_count / total_events
        trusted_rate = trusted_count / total_events

        trust_score = 50
        trust_score += trusted_rate * 40
        trust_score -= suspicious_rate * 50

        trust_score = max(
            0,
            min(100, trust_score)
        )

        cursor.execute("""
            UPDATE identity_memory
            SET login_count = ?,
                suspicious_count = ?,
                trusted_count = ?,
                trust_score = ?,
                last_seen = ?,
                last_status = ?
            WHERE id = ?
        """, (
            login_count,
            suspicious_count,
            trusted_count,
            round(trust_score, 2),
            timestamp,
            decision,
            existing_record["id"]
        ))

    connection.commit()
    connection.close()

    return get_identity_status(
        username,
        ip_address,
        device
    )


# =====================================
# TEST THE MODULE
# =====================================

if __name__ == "__main__":

    status = get_identity_status(
        username="aradhana",
        ip_address="192.168.1.10",
        device="Laptop"
    )

    print("Current Identity Status:", status)

    updated_status = update_identity_memory(
        username="aradhana",
        ip_address="192.168.1.10",
        device="Laptop",
        decision="LOW RISK"
    )

    print("Updated Identity Status:", updated_status)