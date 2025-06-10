from flask import Blueprint, request, jsonify
import uuid
import random

api_bp = Blueprint('api', __name__)

# In-memory session store for demonstration
sessions = {}

@api_bp.route('/start_session', methods=['POST'])
def start_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {'active': True}
    return jsonify({'session_id': session_id}), 200

@api_bp.route('/continue_session', methods=['POST'])
def continue_session():
    data = request.get_json()
    session_id = data.get('session_id')
    if session_id in sessions:
        return jsonify({'message': 'Session continued', 'session_id': session_id}), 200
    else:
        return jsonify({'error': 'Invalid session ID'}), 404

@api_bp.route('/roll_dice', methods=['POST'])
def roll_dice():
    data = request.get_json()
    expr = data.get('expression', '')
    try:
        num, die = expr.lower().split('d')
        num = int(num)
        die = int(die)
        if num < 1 or die < 1 or num > 100:
            raise ValueError
        rolls = [random.randint(1, die) for _ in range(num)]
        return jsonify({'rolls': rolls, 'total': sum(rolls)}), 200
    except Exception:
        return jsonify({'error': 'Invalid dice expression'}), 400
