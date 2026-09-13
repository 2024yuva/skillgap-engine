"""
Database migration script for adding new columns to existing UserCompetency table.

Run this if you have an existing database with the old schema.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "skillgap.db"


def migrate_user_competency_table():
    """Add new columns to user_competencies table for evidence and verification."""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Get existing columns
    cursor.execute("PRAGMA table_info(user_competencies)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    
    new_columns = {
        "verified_level": "INTEGER",
        "evidence": "TEXT",
        "confidence": "REAL DEFAULT 0.5",
        "verification_status": "VARCHAR(50) DEFAULT 'unverified'",
        "last_verified": "DATE",
        "assessment_score": "REAL",
        "assessment_date": "DATE",
    }
    
    for col_name, col_type in new_columns.items():
        if col_name not in existing_columns:
            print(f"Adding column: {col_name} ({col_type})")
            cursor.execute(f"ALTER TABLE user_competencies ADD COLUMN {col_name} {col_type}")
    
    conn.commit()
    conn.close()
    print("Migration complete!")


if __name__ == "__main__":
    migrate_user_competency_table()
