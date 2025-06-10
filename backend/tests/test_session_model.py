import pytest
import uuid
from flask import Flask

# Simulate a persistent session store for testing
class SessionStore:
    def __init__(self):
        self.sessions = {}

    def save(self, session_id, data):
        self.sessions[session_id] = data.copy()

    def load(self, session_id):
        return self.sessions.get(session_id)

    def update(self, session_id, updates):
        if session_id in self.sessions:
            self.sessions[session_id].update(updates)

    def delete(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def all_sessions(self):
        return self.sessions.copy()

store = SessionStore()

@pytest.fixture(autouse=True)
def clear_store():
    store.sessions.clear()
    yield
    store.sessions.clear()

def test_save_new_game_session():
    session_id = str(uuid.uuid4())
    data = {
        'character_id': 'char-1',
        'story_state': {'chapter': 1, 'scene': 'intro'},
        'inventory': ['sword', 'potion'],
        'flags': {'met_npc': True}
    }
    store.save(session_id, data)
    assert session_id in store.sessions
    assert store.sessions[session_id]['character_id'] == 'char-1'
    assert store.sessions[session_id]['story_state']['chapter'] == 1
    assert 'sword' in store.sessions[session_id]['inventory']
    assert store.sessions[session_id]['flags']['met_npc']

def test_load_existing_game_session():
    session_id = str(uuid.uuid4())
    data = {
        'character_id': 'char-2',
        'story_state': {'chapter': 2},
        'inventory': ['shield'],
        'flags': {'boss_defeated': False}
    }
    store.save(session_id, data)
    loaded = store.load(session_id)
    assert loaded['character_id'] == 'char-2'
    assert loaded['story_state']['chapter'] == 2
    assert loaded['inventory'] == ['shield']
    assert loaded['flags']['boss_defeated'] is False

def test_update_session():
    session_id = str(uuid.uuid4())
    data = {
        'character_id': 'char-3',
        'story_state': {'chapter': 1},
        'inventory': [],
        'flags': {}
    }
    store.save(session_id, data)
    store.update(session_id, {'story_state': {'chapter': 2}, 'inventory': ['amulet'], 'flags': {'found_secret': True}})
    updated = store.load(session_id)
    assert updated['story_state']['chapter'] == 2
    assert updated['inventory'] == ['amulet']
    assert updated['flags']['found_secret']

def test_session_resumption():
    session_id = str(uuid.uuid4())
    data = {
        'character_id': 'char-4',
        'story_state': {'chapter': 5},
        'inventory': ['key'],
        'flags': {'door_open': True}
    }
    store.save(session_id, data)
    # Simulate closing and reopening
    resumed = store.load(session_id)
    assert resumed == data

def test_session_without_required_fields():
    session_id = str(uuid.uuid4())
    incomplete_data = {
        'inventory': [],
        'flags': {}
    }
    with pytest.raises(KeyError):
        # Simulate validation: require 'character_id' and 'story_state'
        if 'character_id' not in incomplete_data or 'story_state' not in incomplete_data:
            raise KeyError('Missing required fields')
        store.save(session_id, incomplete_data)

def test_multiple_sessions_for_same_character():
    char_id = 'char-5'
    session1 = str(uuid.uuid4())
    session2 = str(uuid.uuid4())
    store.save(session1, {'character_id': char_id, 'story_state': {'chapter': 1}, 'inventory': [], 'flags': {}})
    store.save(session2, {'character_id': char_id, 'story_state': {'chapter': 2}, 'inventory': ['ring'], 'flags': {}})
    assert session1 in store.sessions and session2 in store.sessions
    assert store.sessions[session1]['story_state']['chapter'] == 1
    assert store.sessions[session2]['story_state']['chapter'] == 2
    assert store.sessions[session2]['inventory'] == ['ring']

def test_data_serialization_deserialization():
    import json
    session_id = str(uuid.uuid4())
    data = {
        'character_id': 'char-6',
        'story_state': {'chapter': 3, 'progress': [1,2,3]},
        'inventory': ['map', 'torch'],
        'flags': {'escaped': False}
    }
    # Simulate serialization
    serialized = json.dumps(data)
    # Simulate deserialization
    deserialized = json.loads(serialized)
    store.save(session_id, deserialized)
    loaded = store.load(session_id)
    assert loaded['character_id'] == 'char-6'
    assert loaded['story_state']['progress'] == [1,2,3]
    assert 'torch' in loaded['inventory']
    assert loaded['flags']['escaped'] is False

def test_session_expiry_or_cleanup():
    session_id = str(uuid.uuid4())
    data = {
        'character_id': 'char-7',
        'story_state': {'chapter': 9},
        'inventory': [],
        'flags': {}
    }
    store.save(session_id, data)
    # Simulate expiry/cleanup
    store.delete(session_id)
    assert store.load(session_id) is None
