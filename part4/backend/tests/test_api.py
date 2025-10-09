import pytest
from app import create_app
from models import db, Player, Quest, Skill
from flask_jwt_extended import create_access_token


@pytest.fixture()
def test_client():
    """Set up a Flask test client with a temporary in-memory DB."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test_secret",
    })

    with app.app_context():
        db.create_all()

        # Create admin and normal user
        admin = Player(name="Admin", class_name="Master", is_admin=True)
        admin.set_password("adminpass")
        user = Player(name="User", class_name="Warrior", is_admin=False)
        user.set_password("userpass")

        db.session.add_all([admin, user])
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def get_token(app, player_name):
    """Generate JWT token for a given player."""
    with app.app_context():
        player = Player.query.filter_by(name=player_name).first()
        return create_access_token(identity=str(player.id))


# =====================================================
# PLAYERS
# =====================================================

def test_get_all_players(test_client):
    """GET /api/players should return all players."""
    token = get_token(test_client.application, "User")
    res = test_client.get(
        "/api/players", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert len(json_data["data"]) == 2


def test_update_player_self(test_client):
    """User should be able to update their own data."""
    app = test_client.application
    token = get_token(app, "User")

    res = test_client.put(
        "/api/players/2",
        headers={"Authorization": f"Bearer {token}"},
        json={"level": 5, "xp": 100}
    )
    json_data = res.get_json()
    assert res.status_code == 200
    assert json_data["success"] is True


def test_delete_player_unauthorized(test_client):
    """User cannot delete another user."""
    app = test_client.application
    token = get_token(app, "User")

    res = test_client.delete(
        "/api/players/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 403


# =====================================================
# QUESTS
# =====================================================

def test_create_quest_admin_only(test_client):
    """Only admin can create a quest."""
    app = test_client.application
    admin_token = get_token(app, "Admin")
    user_token = get_token(app, "User")

    # Non-admin should be denied
    res_user = test_client.post(
        "/api/quests",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Test Quest", "xp": 100}
    )
    assert res_user.status_code == 403

    # Admin should succeed
    res_admin = test_client.post(
        "/api/quests",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"title": "Test Quest", "xp": 100}
    )
    assert res_admin.status_code == 201
    assert res_admin.get_json()["success"] is True


def test_get_quests(test_client):
    """GET /api/quests should return all quests."""
    app = test_client.application
    admin_token = get_token(app, "Admin")

    # Create a quest for testing
    with app.app_context():
        quest = Quest(title="Quest A", xp=50)
        db.session.add(quest)
        db.session.commit()

    res = test_client.get(
        "/api/quests", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert isinstance(data, list)
    assert len(data) >= 1


# =====================================================
# SKILLS
# =====================================================

def test_create_skill_admin_only(test_client):
    """Only admin can create skills."""
    app = test_client.application
    admin_token = get_token(app, "Admin")
    user_token = get_token(app, "User")

    # Unauthorized (user)
    res_user = test_client.post(
        "/api/skills",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Fireball", "level": 3}
    )
    assert res_user.status_code == 403

    # Authorized (admin)
    res_admin = test_client.post(
        "/api/skills",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Fireball", "level": 3}
    )
    assert res_admin.status_code == 201
    assert res_admin.get_json()["success"] is True


def test_get_skills(test_client):
    """GET /api/skills should list skills."""
    app = test_client.application
    admin_token = get_token(app, "Admin")

    with app.app_context():
        skill = Skill(name="Archery", level=2)
        db.session.add(skill)
        db.session.commit()

    res = test_client.get(
        "/api/skills", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert res.get_json()["success"] is True


# =====================================================
# PROGRESS
# =====================================================

def test_get_player_progress(test_client):
    """GET /api/progress/<id> returns player stats."""
    app = test_client.application
    token = get_token(app, "User")

    # Add a quest for player 2 (User)
    with app.app_context():
        quest = Quest(title="Progress Quest", xp=80)
        player = Player.query.filter_by(name="User").first()
        player.quests.append(quest)
        db.session.commit()

    res = test_client.get(
        "/api/progress/2", headers={"Authorization": f"Bearer {token}"})
    json_data = res.get_json()
    assert res.status_code == 200
    assert json_data["success"] is True
    assert json_data["data"]["total_quests_completed"] == 1
    assert json_data["data"]["total_xp_gained"] == 80
