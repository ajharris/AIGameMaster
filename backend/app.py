from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Use PostgreSQL for Heroku deployment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/rpg_db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Importing routes from separate modules
from routes.characters import characters_bp
from routes.systems import systems_bp

app.register_blueprint(characters_bp, url_prefix="/characters")
app.register_blueprint(systems_bp, url_prefix="/systems")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
