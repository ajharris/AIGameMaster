from flask import Blueprint, jsonify

systems_bp = Blueprint("systems", __name__)

@systems_bp.route("/", methods=["GET"])
def get_systems():
    systems = [
        {"name": "D&D 5e", "description": "Dungeons & Dragons 5th Edition"},
        {"name": "Heroes Unlimited", "description": "Superhero RPG"},
        {"name": "Call of Cthulhu", "description": "Horror RPG"}
    ]
    return jsonify(systems)
