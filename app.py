"""
FIELD PLUS — Main Flask Application Factory
Initializes configuration, registers blueprints (auth, admin, worker),
establishes error handlers, and configures diagnostic and landing routes.
"""

import os
from datetime import datetime
from flask import Flask, render_template, jsonify, session, redirect, url_for
from config import config_by_name
from database.db import test_db_connection
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.worker import worker_bp
from routes.tasks import tasks_bp
from routes.attendance import attendance_bp
from routes.leaves import leaves_bp
from routes.notifications import notifications_bp
from routes.api import api_bp
from models.notification import get_unread_count


def create_app(config_name=None):
    """
    Application factory creating and configuring the Flask app instance.
    Args:
        config_name (str, optional): Environment name ('development', 'testing', 'production').
    Returns:
        Flask: Configured application instance.
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development").lower()

    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Load configuration
    config_class = config_by_name.get(config_name, config_by_name["default"])
    app.config.from_object(config_class)

    # --------------------------------------------------------------------------
    # Register Modular Blueprints
    # --------------------------------------------------------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(leaves_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(api_bp)

    # --------------------------------------------------------------------------
    # Global Context Processors (Injected into all Jinja templates)
    # --------------------------------------------------------------------------
    @app.context_processor
    def inject_global_template_variables():
        unread_notifs = 0
        if "user_id" in session:
            try:
                unread_notifs = get_unread_count(session["user_id"])
            except Exception:
                unread_notifs = 0

        return {
            "APP_NAME": app.config.get("APP_NAME", "FIELD PLUS"),
            "APP_TAGLINE": app.config.get("APP_TAGLINE", "Field Work & Task Management System"),
            "CURRENT_YEAR": datetime.now().year,
            "session_user": session.get("user"),
            "session_role": session.get("role"),
            "session_name": session.get("full_name"),
            "unread_notifications_count": unread_notifs,
        }

    # --------------------------------------------------------------------------
    # Custom HTTP Error Handlers
    # --------------------------------------------------------------------------
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500

    # --------------------------------------------------------------------------
    # Core Application Routes
    # --------------------------------------------------------------------------
    @app.route("/")
    def index():
        """Serves the opening animated Field Plus loading screen."""
        if "user_id" in session:
            if session.get("role") == "admin":
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("worker.dashboard"))
        return render_template("splash.html")

    @app.route("/health")
    def health_check():
        """
        Diagnostic API endpoint to verify Flask runtime and MySQL database connectivity.
        """
        db_ok, db_msg = test_db_connection()
        status_code = 200 if db_ok else 503

        return jsonify({
            "status": "healthy" if db_ok else "unhealthy",
            "app": app.config.get("APP_NAME", "FIELD PLUS"),
            "environment": config_name,
            "database": {
                "connected": db_ok,
                "message": db_msg,
                "host": app.config.get("DB_HOST"),
                "name": app.config.get("DB_NAME")
            },
            "server_time": datetime.utcnow().isoformat() + "Z"
        }), status_code

    return app


# ------------------------------------------------------------------------------
# Direct Execution Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    flask_app = create_app()
    port = int(os.getenv("PORT", 5000))
    print(f"\n==================================================")
    print(f"  FIELD PLUS — Field Work Management System")
    print(f"  Running on http://127.0.0.1:{port}/")
    print(f"  Health Check: http://127.0.0.1:{port}/health")
    print(f"==================================================\n")
    flask_app.run(debug=True, host="127.0.0.1", port=port)
