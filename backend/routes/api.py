from flask import Blueprint, request, jsonify, current_app
import uuid
import random
import threading

api_bp = Blueprint('api', __name__)

# In-memory session store for demonstration
sessions = {}
# In-memory kill switch and logs (thread-safe)
_kill_switch = {'enabled': False}
_kill_switch_lock = threading.Lock()
_admin_logs = []
_admin_logs_lock = threading.Lock()

def log_admin(endpoint, input_data, output_data, status):
    with _admin_logs_lock:
        _admin_logs.append({
            'endpoint': endpoint,
            'input': input_data,
            'output': output_data,
            'status': status
        })

@api_bp.route('/kill_switch', methods=['GET', 'POST'])
def kill_switch():
    with _kill_switch_lock:
        if request.method == 'POST':
            data = request.get_json() or {}
            _kill_switch['enabled'] = bool(data.get('enabled', False))
        return jsonify({'enabled': _kill_switch['enabled']}), 200

@api_bp.route('/admin_logs', methods=['GET', 'POST'])
def admin_logs():
    with _admin_logs_lock:
        if request.method == 'POST' and (request.get_json() or {}).get('clear'):
            _admin_logs.clear()
            return jsonify({'logs': []}), 200
        return jsonify({'logs': list(_admin_logs)}), 200

@api_bp.route('/start_session', methods=['POST'])
def start_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {'active': True}
    log_admin('start_session', {}, {'session_id': session_id}, 200)
    return jsonify({'session_id': session_id}), 200

@api_bp.route('/continue_session', methods=['POST'])
def continue_session():
    data = request.get_json()
    session_id = data.get('session_id')
    if session_id in sessions:
        log_admin('continue_session', data, {'message': 'Session continued', 'session_id': session_id}, 200)
        return jsonify({'message': 'Session continued', 'session_id': session_id}), 200
    else:
        log_admin('continue_session', data, {'error': 'Invalid session ID'}, 404)
        return jsonify({'error': 'Invalid session ID'}), 404

@api_bp.route('/roll_dice', methods=['POST'])
def roll_dice():
    with _kill_switch_lock:
        if _kill_switch['enabled']:
            log_admin('roll_dice', request.get_json(), {'error': 'Generation is disabled by admin.'}, 403)
            return jsonify({'error': 'Generation is disabled by admin.'}), 403
    data = request.get_json()
    expr = data.get('expression', '')
    try:
        num, die = expr.lower().split('d')
        num = int(num)
        die = int(die)
        if num < 1 or die < 1 or num > 100:
            raise ValueError
        rolls = [random.randint(1, die) for _ in range(num)]
        result = {'rolls': rolls, 'total': sum(rolls)}
        log_admin('roll_dice', data, result, 200)
        return jsonify(result), 200
    except Exception:
        log_admin('roll_dice', data, {'error': 'Invalid dice expression'}, 400)
        return jsonify({'error': 'Invalid dice expression'}), 400
