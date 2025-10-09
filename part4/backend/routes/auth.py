from flask import Blueprint, request, jsonify
from backend.models import db, Player
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# =====================================================
# Register a new user
# =====================================================


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()

    if not data or "name" not in data or "password" not in data:
        return jsonify({"success": False, "error": "Missing required fields: name, password"}), 400

    if Player.query.filter_by(name=data["name"]).first():
        return jsonify({"success": False, "error": "Username already exists"}), 400

    new_user = Player(
        name=data["name"],
        class_name=data.get("class_name", "Adventurer"),
        level=1,
        xp=0,
        is_admin=False
    )
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "message": "User registered successfully"}), 201


# =====================================================
# Login user and issue JWT
# =====================================================
@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and issue JWT tokens."""
    data = request.get_json()

    if not data or "name" not in data or "password" not in data:
        return jsonify({"success": False, "error": "Missing credentials"}), 400

    user = Player.query.filter_by(name=data["name"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"success": False, "error": "Invalid credentials"}), 401

    # Create short-lived access token and longer refresh token
    access_token = create_access_token(identity=str(
        user.id), expires_delta=timedelta(hours=1))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "class_name": user.class_name,
            "is_admin": user.is_admin
        }
    }), 200


# =====================================================
# Refresh JWT
# =====================================================
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh access token using refresh token."""
    user_id = get_jwt_identity()
    new_access_token = create_access_token(
        identity=user_id, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": new_access_token}), 200


# =====================================================
# Get current logged-in user
# =====================================================
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """Return data about the currently logged-in user."""
    current_user_id = get_jwt_identity()
    user = db.session.get(Player, current_user_id)

    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "class_name": user.class_name,
            "level": user.level,
            "xp": user.xp,
            "is_admin": user.is_admin
        }
    }), 200
