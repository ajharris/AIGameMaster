try:
    from backend.app import db
except ImportError:
    from app import db

class Character(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rpg_system = db.Column(db.String(100), nullable=False)
    data = db.Column(db.JSON, nullable=False)

class Rulebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    rpg_system = db.Column(db.String(100), nullable=True)
    rules = db.Column(db.JSON, nullable=False)
    # Optionally: store upload timestamp, uploader, etc.

class Universe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)

class UserUniverseShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    # Optionally: permissions, timestamps, etc.
