from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import Character
import uuid

characters_bp = Blueprint("characters", __name__)

@characters_bp.route("/", methods=["POST"])
def create_character():
    data = request.json
    new_character = Character(
        id=str(uuid.uuid4()),
        name=data["name"],
        rpg_system=data["rpg_system"],
        data=data["data"]
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"message": "Character created", "character_id": new_character.id}), 201

@characters_bp.route("/<character_id>", methods=["GET"])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"message": "Character not found"}), 404
    return jsonify({"id": character.id, "name": character.name, "rpg_system": character.rpg_system, "data": character.data})
