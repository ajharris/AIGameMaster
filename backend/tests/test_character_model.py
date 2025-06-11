import pytest
import uuid
from backend.models import Character
from backend.app import db

def test_create_character_with_required_fields(app):
    with app.app_context():
        char = Character(
            id=str(uuid.uuid4()),
            name="Test Hero",
            rpg_system="D&D 5e",
            data={
                "attributes": {"strength": 10, "dexterity": 12},
                "skills": ["stealth", "arcana"],
                "powers": ["fireball"],
                "background": "Wanderer"
            }
        )
        db.session.add(char)
        db.session.commit()
        assert Character.query.filter_by(name="Test Hero").first() is not None

def test_retrieve_saved_character(app):
    with app.app_context():
        char = Character(
            id=str(uuid.uuid4()),
            name="Retrieve Hero",
            rpg_system="D&D 5e",
            data={"attributes": {"intelligence": 15}, "skills": [], "powers": [], "background": "Sage"}
        )
        db.session.add(char)
        db.session.commit()
        found = Character.query.get(char.id)
        assert found is not None
        assert found.name == "Retrieve Hero"
        assert found.data["attributes"]["intelligence"] == 15

def test_prevent_character_creation_without_required_fields(app):
    with app.app_context():
        with pytest.raises(Exception):
            char = Character(
                id=str(uuid.uuid4()),
                name=None,
                rpg_system="D&D 5e",
                data={}
            )
            db.session.add(char)
            db.session.commit()

def test_guided_character_creation(app):
    with app.app_context():
        template = {
            "attributes": {"strength": 8, "wisdom": 14},
            "skills": ["insight"],
            "powers": ["healing word"],
            "background": "Cleric"
        }
        char = Character(
            id=str(uuid.uuid4()),
            name="Guided Hero",
            rpg_system="D&D 5e",
            data=template
        )
        db.session.add(char)
        db.session.commit()
        found = Character.query.filter_by(name="Guided Hero").first()
        assert found is not None
        assert found.data["background"] == "Cleric"

def test_manual_character_creation(app):
    with app.app_context():
        manual_data = {
            "attributes": {"charisma": 16},
            "skills": ["persuasion"],
            "powers": [],
            "background": "Bard"
        }
        char = Character(
            id=str(uuid.uuid4()),
            name="Manual Hero",
            rpg_system="D&D 5e",
            data=manual_data
        )
        db.session.add(char)
        db.session.commit()
        found = Character.query.filter_by(name="Manual Hero").first()
        assert found is not None
        assert found.data["attributes"]["charisma"] == 16

def test_add_custom_attribute_column(app):
    with app.app_context():
        # Add a custom attribute to the data JSON
        char = Character(
            id=str(uuid.uuid4()),
            name="Mutant Hero",
            rpg_system="Mutants & Masterminds",
            data={
                "attributes": {"mutationLevel": 5},
                "skills": [],
                "powers": ["regeneration"],
                "background": "Experiment"
            }
        )
        db.session.add(char)
        db.session.commit()
        found = Character.query.filter_by(name="Mutant Hero").first()
        assert found.data["attributes"]["mutationLevel"] == 5

def test_save_and_retrieve_custom_attribute_value(app):
    with app.app_context():
        char = Character(
            id=str(uuid.uuid4()),
            name="Lucky Hero",
            rpg_system="D&D 5e",
            data={
                "attributes": {"luck": 13},
                "skills": [],
                "powers": [],
                "background": "Gambler"
            }
        )
        db.session.add(char)
        db.session.commit()
        found = Character.query.filter_by(name="Lucky Hero").first()
        assert found.data["attributes"]["luck"] == 13

def test_multiple_characters_with_different_custom_attributes(app):
    with app.app_context():
        char1 = Character(
            id=str(uuid.uuid4()),
            name="Hero One",
            rpg_system="System A",
            data={"attributes": {"luck": 7}, "skills": [], "powers": [], "background": "A"}
        )
        char2 = Character(
            id=str(uuid.uuid4()),
            name="Hero Two",
            rpg_system="System B",
            data={"attributes": {"mutationLevel": 3}, "skills": [], "powers": [], "background": "B"}
        )
        db.session.add(char1)
        db.session.add(char2)
        db.session.commit()
        found1 = Character.query.filter_by(name="Hero One").first()
        found2 = Character.query.filter_by(name="Hero Two").first()
        assert found1.data["attributes"]["luck"] == 7
        assert found2.data["attributes"]["mutationLevel"] == 3

def test_sqlite_compatibility(tmp_path, app):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from backend.models import Character, db
    import os
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Session = sessionmaker(bind=engine)
    db.Model.metadata.create_all(engine)
    session = Session()
    char = Character(
        id=str(uuid.uuid4()),
        name="SQLite Hero",
        rpg_system="D&D 5e",
        data={"attributes": {"strength": 10}, "skills": [], "powers": [], "background": "Test"}
    )
    session.add(char)
    session.commit()
    found = session.query(Character).filter_by(name="SQLite Hero").first()
    assert found is not None
    assert found.data["attributes"]["strength"] == 10
    session.close()

def test_postgresql_compatibility(app):
    # This test assumes the default DATABASE_URL is PostgreSQL and the db is available
    with app.app_context():
        char = Character(
            id=str(uuid.uuid4()),
            name="Postgres Hero",
            rpg_system="D&D 5e",
            data={"attributes": {"strength": 18}, "skills": [], "powers": [], "background": "Test"}
        )
        db.session.add(char)
        db.session.commit()
        found = Character.query.filter_by(name="Postgres Hero").first()
        assert found is not None
        assert found.data["attributes"]["strength"] == 18
