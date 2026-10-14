import sqlite3
from pathlib import Path
from datetime import datetime


# ==========================================
# DATABASE PATH
# ==========================================

project_folder = Path(__file__).resolve().parent
database_path = project_folder / "project_memory.db"


# ==========================================
# SAVE DECISION CORRECTION
# ==========================================

def save_decision_correction(
    original_decision,
    corrected_decision,
    reason,
    username="unknown",
    source_ip="unknown",
    confidence_change=0.0
):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO decision_recovery_memory
        (
            timestamp,
            original_decision,
            corrected_decision,
            reason,
            source_ip,
            username,
            confidence_change
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        original_decision,
        corrected_decision,
        reason,
        source_ip,
        username,
        confidence_change
    ))

    connection.commit()
    connection.close()

    print("Decision correction saved successfully!")


# ==========================================
# GET PREVIOUS DECISION CORRECTIONS
# ==========================================

def get_previous_corrections(username=None, source_ip=None):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if username and source_ip:
        cursor.execute("""
            SELECT *
            FROM decision_recovery_memory
            WHERE username = ? AND source_ip = ?
            ORDER BY id DESC
        """, (username, source_ip))

    elif username:
        cursor.execute("""
            SELECT *
            FROM decision_recovery_memory
            WHERE username = ?
            ORDER BY id DESC
        """, (username,))

    elif source_ip:
        cursor.execute("""
            SELECT *
            FROM decision_recovery_memory
            WHERE source_ip = ?
            ORDER BY id DESC
        """, (source_ip,))

    else:
        cursor.execute("""
            SELECT *
            FROM decision_recovery_memory
            ORDER BY id DESC
        """)

    corrections = cursor.fetchall()
    connection.close()

    return corrections


# ==========================================
# TEST DECISION RECOVERY MEMORY
# ==========================================

if __name__ == "__main__":

    save_decision_correction(
        original_decision="LOW RISK",
        corrected_decision="HIGH RISK",
        reason="Repeated failed login attempts were detected later",
        username="aradhana",
        source_ip="192.168.1.10",
        confidence_change=65.5
    )

    corrections = get_previous_corrections(
        username="aradhana",
        source_ip="192.168.1.10"
    )

    print("\nPrevious Decision Corrections:")

    for correction in corrections:
        print("------------------------------")
        print("Time:", correction["timestamp"])
        print("Original Decision:", correction["original_decision"])
        print("Corrected Decision:", correction["corrected_decision"])
        print("Reason:", correction["reason"])
        print("Username:", correction["username"])
        print("Source IP:", correction["source_ip"])
        print("Confidence Change:", correction["confidence_change"])