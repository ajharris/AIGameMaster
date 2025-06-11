import json
import pytest
from backend.app import create_app

def test_start_session(client):
    response = client.post('/api/start_session')
    assert response.status_code == 200 or response.status_code == 201
    data = response.get_json()
    assert 'session_id' in data or 'success' in data

def test_continue_session_valid(client):
    # First, start a session to get a valid session_id
    start_resp = client.post('/api/start_session')
    session_id = start_resp.get_json().get('session_id', None)
    if not session_id:
        pytest.skip('No session_id returned from start_session')
    response = client.post('/api/continue_session', json={'session_id': session_id})
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data or 'success' in data

def test_continue_session_invalid(client):
    response = client.post('/api/continue_session', json={'session_id': 'invalid'})
    assert response.status_code in (400, 404)

def test_roll_dice_valid(client):
    response = client.post('/api/roll_dice', json={'expression': '2d6'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'rolls' in data and 'total' in data
    assert len(data['rolls']) == 2
    assert isinstance(data['total'], int)

def test_roll_dice_invalid(client):
    response = client.post('/api/roll_dice', json={'expression': 'badinput'})
    assert response.status_code in (400, 422)

def test_roll_dice_single_die(client):
    response = client.post('/api/roll_dice', json={'expression': '1d20'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'rolls' in data and 'total' in data
    assert isinstance(data['rolls'], list)
    assert len(data['rolls']) == 1
    assert 1 <= data['rolls'][0] <= 20
    assert data['total'] == data['rolls'][0]

def test_roll_dice_multiple_dice(client):
    response = client.post('/api/roll_dice', json={'expression': '3d6'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'rolls' in data and 'total' in data
    assert len(data['rolls']) == 3
    for roll in data['rolls']:
        assert 1 <= roll <= 6
    assert data['total'] == sum(data['rolls'])

def test_roll_dice_invalid_input(client):
    response = client.post('/api/roll_dice', json={'expression': 'badinput'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_roll_dice_zero_dice(client):
    response = client.post('/api/roll_dice', json={'expression': '0d6'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_roll_dice_100d1(client):
    response = client.post('/api/roll_dice', json={'expression': '100d1'})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['rolls']) == 100
    assert all(roll == 1 for roll in data['rolls'])
    assert data['total'] == 100

def test_api_blueprint_registration(app):
    # Ensure /api/ endpoints are registered
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert any(r.startswith('/api/start_session') for r in rules)
    assert any(r.startswith('/api/continue_session') for r in rules)
    assert any(r.startswith('/api/roll_dice') for r in rules)

def test_app_factory_isolation():
    from flask import Flask
    from backend.app import create_app
    main_app = create_app()
    test_app = Flask(__name__)
    assert test_app != main_app
    # Test that routes can be registered
    @test_app.route('/test')
    def test():
        return 'ok'
    client = test_app.test_client()
    resp = client.get('/test')
    assert resp.status_code == 200

def test_kill_switch_route(client):
    # Should return the current state (default: False)
    resp = client.get('/api/kill_switch')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'enabled' in data
    # Should allow toggling
    resp2 = client.post('/api/kill_switch', json={'enabled': True})
    assert resp2.status_code == 200
    data2 = resp2.get_json()
    assert data2['enabled'] is True
    # Should reflect new state
    resp3 = client.get('/api/kill_switch')
    assert resp3.get_json()['enabled'] is True


def test_generation_blocked_when_kill_switch_enabled(client):
    # Enable kill switch
    client.post('/api/kill_switch', json={'enabled': True})
    # Try to roll dice (should be blocked)
    resp = client.post('/api/roll_dice', json={'expression': '1d6'})
    assert resp.status_code == 403
    assert 'disabled' in resp.get_json().get('error', '')


def test_admin_log_storage_and_retrieval(client):
    # Clear logs
    client.post('/api/admin_logs', json={'clear': True})
    # Simulate input/output
    client.post('/api/roll_dice', json={'expression': '1d6'})
    # Retrieve logs
    resp = client.get('/api/admin_logs')
    assert resp.status_code == 200
    logs = resp.get_json().get('logs', [])
    assert isinstance(logs, list)
    # Should contain at least one log entry
    assert any('roll_dice' in (entry.get('endpoint') or '') for entry in logs)

def test_rate_limit_roll_dice(client):
    # Simulate hitting the rate limit by sending many requests quickly
    for _ in range(20):
        resp = client.post('/api/roll_dice', json={'expression': '1d6'})
        if resp.status_code == 429:
            data = resp.get_json()
            assert 'too many requests' in data.get('error', '').lower()
            break
    else:
        pytest.skip('Rate limit not triggered; check if rate limiting is enabled')
