import pytest
from flask import Flask
from app.blueprints.home.routes import show_user_profile
from app.blueprints.home import home_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("username, expected_response", [
    ("john_doe", "User john_doe"),
    ("jane_doe", "User jane_doe"),
    ("John Doe", "User John Doe"),
    ("user123", "User user123"),
    ("a" * 256, f"User {'a' * 256}"),
], ids=[
    "happy_path_john_doe",
    "happy_path_jane_doe",
    "happy_user_with_spaces",
    "happy_path_user123",
    "edge_case_long_username",
])
def test_show_user_profile(client, username, expected_response):

    # Act
    response = client.get(f'/user/{username}')
    
    print(response.status_code)

    # Assert
    assert response.status_code == 200
    assert response.data.decode('utf-8') == expected_response

@pytest.mark.parametrize("username", [
    ("<script>alert('xss')</script>"),
    (""),
    ("user/with/slash"),
], ids=[
    "error_case_xss",
    "error_empty_username",
    "error_case_slash",
])
def test_show_user_profile_error_cases(client, username):

    # Act
    response = client.get(f'/user/{username}')

    # Assert
    assert response.status_code == 404
