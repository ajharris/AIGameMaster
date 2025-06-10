from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import subprocess

db = SQLAlchemy()

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

    if test_config is not None:
        app.config.update(test_config)
    else:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/rpg_db")
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Importing routes from separate modules
    from backend.routes.characters import characters_bp
    from backend.routes.systems import systems_bp
    from backend.routes.api import api_bp

    app.register_blueprint(characters_bp, url_prefix="/characters")
    app.register_blueprint(systems_bp, url_prefix="/systems")
    app.register_blueprint(api_bp, url_prefix="/api")

    # Serve React frontend
    from flask import send_from_directory

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        if path.startswith("api") or path.startswith("characters") or path.startswith("systems"):
            # Let API routes be handled by blueprints
            return ("", 404)
        full_path = os.path.normpath(os.path.join(app.static_folder, path))
        if not full_path.startswith(app.static_folder):
            return ("", 404)
        if path != "" and os.path.exists(full_path):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    app.run(debug=(FLASK_ENV == "development"))
