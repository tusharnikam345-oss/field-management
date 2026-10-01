"""
FIELD PLUS — Migration: Add Admin-Worker Isolation
Adds `created_by_admin_id` column to the workers table so each admin
can only see their own workers.
"""

import pymysql
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def run_migration():
    print("\n" + "=" * 55)
    print("  FIELD PLUS — Admin-Worker Isolation Migration")
    print("=" * 55)

    try:
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Tushar@123",
            database="field_plus_db",
            charset="utf8mb4",
            autocommit=True
        )
        print("  Connected to MySQL.")
    except Exception as e:
        print(f"  ERROR: Could not connect - {e}")
        return False

    cur = conn.cursor()

    # 1. Check if column already exists
    cur.execute("""
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'field_plus_db'
          AND TABLE_NAME = 'workers'
          AND COLUMN_NAME = 'created_by_admin_id';
    """)
    if cur.fetchone():
        print("  Column 'created_by_admin_id' already exists. Skipping ALTER.")
    else:
        print("  Adding 'created_by_admin_id' column to workers table...")
        cur.execute("""
            ALTER TABLE workers
            ADD COLUMN created_by_admin_id INT NULL AFTER status,
            ADD INDEX idx_workers_admin (created_by_admin_id),
            ADD CONSTRAINT fk_workers_created_by_admin
                FOREIGN KEY (created_by_admin_id) REFERENCES admins(id)
                ON DELETE SET NULL ON UPDATE CASCADE;
        """)
        print("  Column added successfully!")

    # 2. Assign existing workers to the first admin (id=1)
    cur.execute("SELECT id FROM admins ORDER BY id LIMIT 1;")
    first_admin = cur.fetchone()
    if first_admin:
        admin_id = first_admin[0]
        cur.execute(
            "UPDATE workers SET created_by_admin_id = %s WHERE created_by_admin_id IS NULL;",
            (admin_id,)
        )
        print(f"  Assigned all existing workers to admin id={admin_id}.")
    
    conn.close()
    print("\n  Migration COMPLETE!")
    print("=" * 55 + "\n")
    return True


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
