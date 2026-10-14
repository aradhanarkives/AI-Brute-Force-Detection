import sqlite3
from pathlib import Path


project_folder = Path(__file__).resolve().parent
database_path = project_folder / "project_memory.db"


def save_decision_correction(
    original_decision,
    corrected_decision,
    reason
):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO decision_recovery_memory
        (
            original_decision,
            corrected_decision,
            reason
        )
        VALUES (?, ?, ?)
    """, (
        original_decision,
        corrected_decision,
        reason
    ))

    connection.commit()
    connection.close()

    print("Decision correction saved successfully!")


save_decision_correction(
    original_decision="LOW RISK",
    corrected_decision="HIGH RISK",
    reason="The identity later showed repeated suspicious login behavior"
)