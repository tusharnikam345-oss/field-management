"""
FIELD PLUS — CLI Management Utility
Provides convenience commands familiar to developers and students.
Usage:
    python manage.py runserver       # Starts local development server on port 5000
    python manage.py runserver 8000  # Starts on custom port (e.g. 8000)
    python manage.py test            # Runs the complete 49-test verification suite
"""

import sys
import os
from app import create_app


def main():
    args = sys.argv[1:]
    command = args[0].lower() if args else "runserver"

    if command == "runserver":
        port = int(os.getenv("PORT", 5000))
        if len(args) > 1:
            try:
                port = int(args[1])
            except ValueError:
                print(f"[Warning] Invalid port '{args[1]}', falling back to default {port}.")

        app = create_app("development")
        print("\n" + "=" * 55)
        print("  FIELD PLUS — Field Work Management System")
        print(f"  Local Development Server: http://127.0.0.1:{port}/")
        print(f"  Health Check Diagnostics: http://127.0.0.1:{port}/health")
        print("=" * 55 + "\n")
        app.run(debug=True, host="127.0.0.1", port=port)

    elif command in ("test", "tests"):
        import run_tests
        sys.exit(run_tests.run_all_tests())

    else:
        print(f"Unknown command '{command}'.")
        print("Available commands:")
        print("  python manage.py runserver [port]   - Run local web server")
        print("  python manage.py test               - Run all automated tests")


if __name__ == "__main__":
    main()
