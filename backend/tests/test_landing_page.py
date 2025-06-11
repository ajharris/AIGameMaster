import os
import tempfile
import shutil
import pytest
from backend.app import create_app

def client(app):
    app.static_folder = tempfile.mkdtemp()
    with open(os.path.join(app.static_folder, 'index.html'), 'w') as f:
        f.write('<html><body>Landing Page</body></html>')
    with app.test_client() as client:
        yield client
    shutil.rmtree(app.static_folder)

def test_landing_page_served(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Landing Page' in resp.data

def test_404_for_invalid_path(client):
    resp = client.get('/notarealpage')
    assert resp.status_code == 200 or resp.status_code == 404
    # If not found, should serve index.html (SPA fallback) or 404
    if resp.status_code == 200:
        assert b'Landing Page' in resp.data
