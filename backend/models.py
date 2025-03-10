from backend.app import db

class Character(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rpg_system = db.Column(db.String(100), nullable=False)
    data = db.Column(db.JSON, nullable=False)
