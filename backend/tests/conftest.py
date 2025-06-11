import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from flask import Flask
from backend.app import create_app
import subprocess
import tempfile
import shutil
from alembic.config import Config
from alembic import command


@pytest.fixture(scope="function")
def app():
    # Create a temp file-based SQLite DB for Alembic compatibility
    db_dir = tempfile.mkdtemp()
    db_path = os.path.join(db_dir, 'test.db')
    db_uri = f"sqlite:///{db_path}"
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": db_uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "TESTING": True
    })
    # Run Alembic migrations to create all tables
    with app.app_context():
        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '../../migrations/alembic.ini'))
        alembic_cfg.set_main_option('sqlalchemy.url', db_uri)
        # Set script_location explicitly for Alembic
        migrations_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../migrations'))
        alembic_cfg.set_main_option('script_location', migrations_path)
        command.upgrade(alembic_cfg, 'head')
        yield app
    shutil.rmtree(db_dir)

@pytest.fixture
def client(app):
    return app.test_client()
