# tests/conftest.py
import os
import pytest
import sys


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
    
from app import create_app, db


print(sys.path)

@pytest.fixture
def app():
    app = create_app('testing')  # Use the 'testing' config for a test-specific setup
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
