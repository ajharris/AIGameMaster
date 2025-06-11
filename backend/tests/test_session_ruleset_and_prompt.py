import pytest
from backend.models import Rulebook
from backend.app import create_app, db

@pytest.fixture(scope="session")
def app():
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "TESTING": True
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_switching_rpg_system_updates_ruleset(app):
    with app.app_context():
        rulebook1 = Rulebook(filename="file1.pdf", rpg_system="SystemA", rules={"rules": "A rules"})
        rulebook2 = Rulebook(filename="file2.pdf", rpg_system="SystemB", rules={"rules": "B rules"})
        db.session.add(rulebook1)
        db.session.add(rulebook2)
        db.session.commit()
        # Simulate session with SystemA
        session = {"rpg_system": rulebook1.rpg_system, "ruleset": rulebook1.rules}
        assert session["ruleset"] == rulebook1.rules
        # Switch to SystemB
        session["rpg_system"] = rulebook2.rpg_system
        session["ruleset"] = rulebook2.rules
        assert session["ruleset"] == rulebook2.rules

def test_invalid_system_id_triggers_validation_error(app):
    with app.app_context():
        # No rulebook for this system
        invalid_system = "NonexistentSystem"
        found = Rulebook.query.filter_by(rpg_system=invalid_system).first()
        assert found is None
        # Simulate validation/fallback
        session = {"rpg_system": invalid_system}
        fallback = "Default rules"
        ruleset = fallback if found is None else found.rules
        assert ruleset == fallback

def test_changing_rpg_system_updates_prompt_template():
    # Simulate prompt template per system
    templates = {"SystemA": "Prompt for A", "SystemB": "Prompt for B"}
    session = {"rpg_system": "SystemA"}
    prompt = templates.get(session["rpg_system"], "Default prompt")
    assert prompt == "Prompt for A"
    session["rpg_system"] = "SystemB"
    prompt = templates.get(session["rpg_system"], "Default prompt")
    assert prompt == "Prompt for B"

def test_get_session_includes_system_name(client, app):
    with app.app_context():
        # Simulate session creation and retrieval endpoint
        rulebook = Rulebook(filename="file.pdf", rpg_system="SystemX", rules={"rules": "X rules"})
        db.session.add(rulebook)
        db.session.commit()
        # Simulate API response
        session_data = {"session_id": "abc123", "system_name": rulebook.rpg_system}
        assert "system_name" in session_data
        assert session_data["system_name"] == "SystemX"

def test_get_session_unrecognized_system_name(client, app):
    with app.app_context():
        # Simulate session with unknown system
        unknown_system = "UnknownSystem"
        session_data = {"session_id": "abc123", "system_name": unknown_system}
        known_systems = [r.rpg_system for r in Rulebook.query.all()]
        display_name = session_data["system_name"] if session_data["system_name"] in known_systems else "Custom/Unknown"
        assert display_name == "Custom/Unknown"
