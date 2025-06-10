from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
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

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    app.run(debug=(FLASK_ENV == "development"))
