import pytest
from app import create_app
from models import db, Player
from flask_jwt_extended import create_access_token


@pytest.fixture()
def test_client():
    """Set up a Flask test client with an in-memory SQLite DB."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test_secret",
    })

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_register_and_login(test_client):
    """Test user registration and login."""
    # Register a new user
    register_data = {"name": "Tester", "password": "1234"}
    res = test_client.post("/auth/register", json=register_data)
    assert res.status_code == 201

    # Login with the new user
    login_data = {"name": "Tester", "password": "1234"}
    res = test_client.post("/auth/login", json=login_data)
    json_data = res.get_json()
    assert res.status_code == 200
    assert "access_token" in json_data
    assert json_data["success"] is True


def test_me_endpoint(test_client):
    """Test fetching current user info."""
    with test_client.application.app_context():
        user = Player(name="UserX", class_name="Rogue", is_admin=False)
        user.set_password("pass")
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=str(user.id))

    res = test_client.get(
        "/auth/me", headers={"Authorization": f"Bearer {token}"})
    json_data = res.get_json()
    assert res.status_code == 200
    assert json_data["success"] is True
    assert json_data["user"]["name"] == "UserX"
