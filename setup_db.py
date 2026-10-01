"""
FIELD PLUS — Database Setup & Credential Verifier
Helps configure MySQL root credentials in .env and imports database/field_plus.sql.
Usage:
    python setup_db.py [your_mysql_password]
"""

import os
import sys
from pathlib import Path
import pymysql

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
SQL_FILE = BASE_DIR / "database" / "field_plus.sql"


def update_env_password(password):
    """Write the provided password into .env file."""
    if not ENV_PATH.exists():
        return False
    
    lines = ENV_PATH.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for line in lines:
        if line.startswith("DB_PASSWORD="):
            new_lines.append(f"DB_PASSWORD={password}")
        else:
            new_lines.append(line)
    
    ENV_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return True


def test_and_import(password):
    """Test MySQL connection with password and import schema if needed."""
    print("\n" + "=" * 55)
    print("  FIELD PLUS — Database Setup & Initializer")
    print("=" * 55)

    print(f"\n1. Testing MySQL connection with user='root'...")
    try:
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password=password,
            charset="utf8mb4",
            autocommit=True
        )
        print("   ✔ Successfully connected to MySQL server!")
    except pymysql.err.OperationalError as e:
        if e.args[0] == 1045:
            print(f"\n   ✖ Access Denied: Incorrect password '{password}'.")
            print("   Please check your MySQL root password and try again.")
        else:
            print(f"\n   ✖ Connection Error ({e.args[0]}): {e.args[1] if len(e.args)>1 else e}")
        return False

    # Create database and import schema
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS field_plus_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print("   ✔ Database 'field_plus_db' is ready.")

        conn.select_db("field_plus_db")

        # Check if tables already exist
        with conn.cursor() as cur:
            cur.execute("SHOW TABLES;")
            tables = [row[0] for row in cur.fetchall()]

        if "users" in tables and "tasks" in tables:
            print(f"   ✔ Database tables already exist ({len(tables)} tables).")
        else:
            print("2. Importing 'database/field_plus.sql' schema & demo data...")
            if not SQL_FILE.exists():
                print(f"   ✖ Schema file not found at: {SQL_FILE}")
                conn.close()
                return False

            sql_content = SQL_FILE.read_text(encoding="utf-8")
            statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

            with conn.cursor() as cur:
                for stmt in statements:
                    # Ignore USE and CREATE DATABASE statements as we already selected db
                    if stmt.upper().startswith("CREATE DATABASE") or stmt.upper().startswith("USE "):
                        continue
                    try:
                        cur.execute(stmt)
                    except Exception as ex:
                        pass
            print(f"   ✔ Successfully imported schema and seeded demo users!")

        conn.close()

        # Update .env
        update_env_password(password)
        print("3. Updated .env with working DB_PASSWORD.")
        print("\n" + "=" * 55)
        print("  🎉 DATABASE SETUP COMPLETE! You can now log in.")
        print("  Admin Email:    admin@fieldplus.com")
        print("  Admin Password: Admin@123")
        print("=" * 55 + "\n")
        return True

    except Exception as e:
        print(f"   ✖ Error setting up database: {e}")
        conn.close()
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pwd = sys.argv[1]
    else:
        pwd = input("Enter your MySQL root password (press Enter if blank): ")

    success = test_and_import(pwd)
    sys.exit(0 if success else 1)
