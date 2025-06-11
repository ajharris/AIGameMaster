from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import subprocess
import sys
import logging

db = SQLAlchemy()
migrate = Migrate()

# Limiter instance for use in routes
limiter = Limiter(get_remote_address, default_limits=["100 per hour"])

# Ensure 'backend' is in sys.path for all entrypoints
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure the frontend is built before starting in production (Heroku)
def build_frontend_if_needed():
    if os.environ.get("FLASK_ENV") == "production":
        dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/dist"))
        index_html = os.path.join(dist_path, "index.html")
        if not os.path.exists(dist_path) or not os.path.exists(index_html):
            frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
            try:
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
                subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
            except Exception as e:
                print(f"[ERROR] Could not build frontend: {e}")

def create_app(test_config=None):
    build_frontend_if_needed()
    app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
    CORS(app)

    limiter.init_app(app)

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return (jsonify(error="Too many requests, slow down!"), 429)

    if test_config is not None:
        app.config.update(test_config)
    else:
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            # Use SQLite for local dev if not specified
            DATABASE_URL = "sqlite:///../instance/dev.db"
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    # For tests: create all tables in the test DB (handled by Alembic in conftest.py)
    if test_config is not None:
        # Do not call db.create_all() or check for Rulebook in test mode
        pass
    else:
        # Only insert dummy data in non-test mode and inside app context, if table exists
        with app.app_context():
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            if 'rulebook' in inspector.get_table_names():
                from backend.models import Rulebook
                if not Rulebook.query.first():
                    dummy = Rulebook(filename="dummy.txt", rpg_system="DummySystem", rules={"rules": "Dummy rules", "sections": ["Dummy section"], "tables": []})
                    db.session.add(dummy)
                    db.session.commit()

    # Importing routes from separate modules
    from backend.routes.characters import characters_bp
    from backend.routes.systems import systems_bp
    from backend.routes.api import api_bp
    from backend.routes.upload_rulebook import upload_rulebook_bp

    app.register_blueprint(characters_bp, url_prefix="/characters")
    app.register_blueprint(systems_bp, url_prefix="/systems")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(upload_rulebook_bp)

    # Serve React frontend
    from flask import send_from_directory

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        # Only block API/blueprint routes
        if path.startswith("api") or path.startswith("characters") or path.startswith("systems"):
            return ("", 404)
        # Try to serve the static file if it exists
        full_path = os.path.realpath(os.path.join(app.static_folder, path))
        # Only allow serving files strictly within the static folder
        if os.path.isfile(full_path) and os.path.commonpath([full_path, os.path.realpath(app.static_folder)]) == os.path.realpath(app.static_folder):
            return send_from_directory(app.static_folder, os.path.relpath(full_path, app.static_folder))
        # Fallback: always serve index.html for SPA
        return send_from_directory(app.static_folder, "index.html")

    return app

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    app = create_app()
    # Do not call db.create_all() here; use migrations for schema management
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    app.run(debug=(FLASK_ENV == "development"))
