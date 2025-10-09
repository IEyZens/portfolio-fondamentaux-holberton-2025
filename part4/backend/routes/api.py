from flask import Blueprint, jsonify, request
from backend.models import db, Player, Quest, Skill
from backend.utils.auth_decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity

api_bp = Blueprint('api', __name__)

# =====================================================
# Helper functions
# =====================================================


def success_response(data, status_code=200):
    """Return a consistent success JSON response."""
    return jsonify({"success": True, "data": data}), status_code


def error_response(message, status_code=400):
    """Return a consistent error JSON response."""
    return jsonify({"success": False, "error": message}), status_code

# =====================================================
# PLAYERS
# =====================================================


@api_bp.route('/players', methods=['GET'])
@jwt_required()
def get_players():
    """Get all players (authenticated users)."""
    players = Player.query.all()
    return success_response([p.to_dict(False) for p in players])


@api_bp.route('/players/<int:player_id>', methods=['GET'])
@jwt_required()
def get_player(player_id):
    """Get a player by ID."""
    player = db.session.get(Player, player_id)
    if not player:
        return error_response("Player not found", 404)
    return success_response(player.to_dict())


@api_bp.route('/players', methods=['POST'])
def create_player():
    """Create a new player (public endpoint)."""
    data = request.get_json()
    if not data or "name" not in data or "class_name" not in data:
        return error_response("Missing required fields: name, class_name", 400)

    new_player = Player(
        name=data["name"],
        class_name=data["class_name"],
        level=data.get("level", 1),
        xp=data.get("xp", 0),
        is_admin=data.get("is_admin", False)
    )
    db.session.add(new_player)
    db.session.commit()

    return success_response({"message": "Player created successfully", "id": new_player.id}, 201)


@api_bp.route('/players/<int:player_id>', methods=['PUT'])
@jwt_required()
def update_player(player_id):
    """Update player info (admin or owner only)."""
    current_user = db.session.get(Player, get_jwt_identity())
    player = db.session.get(Player, player_id)

    if not player:
        return error_response("Player not found", 404)
    if not current_user.is_admin and current_user.id != player.id:
        return error_response("You are not authorized to update this player", 403)

    data = request.get_json()
    if not data:
        return error_response("No data provided", 400)

    player.name = data.get("name", player.name)
    player.class_name = data.get("class_name", player.class_name)
    player.level = data.get("level", player.level)
    player.xp = data.get("xp", player.xp)
    db.session.commit()

    return success_response({"message": "Player updated successfully", "player": player.to_dict()})


@api_bp.route('/players/<int:player_id>', methods=['DELETE'])
@jwt_required()
def delete_player(player_id):
    """Delete player (admin or owner only)."""
    current_user = db.session.get(Player, get_jwt_identity())
    player = db.session.get(Player, player_id)

    if not player:
        return error_response("Player not found", 404)
    if not current_user.is_admin and current_user.id != player.id:
        return error_response("You are not authorized to delete this player", 403)

    db.session.delete(player)
    db.session.commit()
    return success_response({"message": "Player deleted successfully"})

# =====================================================
# QUESTS
# =====================================================


@api_bp.route('/quests', methods=['GET'])
@jwt_required()
def get_quests():
    """Get all quests (authenticated users)."""
    quests = Quest.query.all()
    return success_response([q.to_dict(False) for q in quests])


@api_bp.route('/quests/<int:quest_id>', methods=['GET'])
@jwt_required()
def get_quest(quest_id):
    """Get a quest by ID."""
    quest = db.session.get(Quest, quest_id)
    if not quest:
        return error_response("Quest not found", 404)
    return success_response(quest.to_dict())


@api_bp.route('/quests', methods=['POST'])
@admin_required
def create_quest():
    """Create a quest (admin only)."""
    data = request.get_json()
    if not data or "title" not in data or "xp" not in data:
        return error_response("Missing required fields: title, xp", 400)

    new_quest = Quest(
        title=data["title"],
        xp=data["xp"],
        summary=data.get("summary", "")
    )
    db.session.add(new_quest)
    db.session.commit()
    return success_response({"message": "Quest created successfully", "id": new_quest.id}, 201)


@api_bp.route('/quests/<int:quest_id>', methods=['PUT'])
@admin_required
def update_quest(quest_id):
    """Update a quest (admin only)."""
    quest = db.session.get(Quest, quest_id)
    if not quest:
        return error_response("Quest not found", 404)

    data = request.get_json()
    if not data:
        return error_response("No data provided", 400)

    quest.title = data.get("title", quest.title)
    quest.xp = data.get("xp", quest.xp)
    quest.summary = data.get("summary", quest.summary)
    db.session.commit()

    return success_response({"message": "Quest updated successfully", "quest": quest.to_dict()})


@api_bp.route('/quests/<int:quest_id>', methods=['DELETE'])
@admin_required
def delete_quest(quest_id):
    """Delete a quest (admin only)."""
    quest = db.session.get(Quest, quest_id)
    if not quest:
        return error_response("Quest not found", 404)

    db.session.delete(quest)
    db.session.commit()
    return success_response({"message": "Quest deleted successfully"})

# =====================================================
# SKILLS
# =====================================================


@api_bp.route('/skills', methods=['GET'])
@jwt_required()
def get_skills():
    """Get all skills (authenticated users)."""
    skills = Skill.query.all()
    return success_response([s.to_dict(False) for s in skills])


@api_bp.route('/skills/<int:skill_id>', methods=['GET'])
@jwt_required()
def get_skill(skill_id):
    """Get a skill by ID."""
    skill = db.session.get(Skill, skill_id)
    if not skill:
        return error_response("Skill not found", 404)
    return success_response(skill.to_dict())


@api_bp.route('/skills', methods=['POST'])
@admin_required
def create_skill():
    """Create a skill (admin only)."""
    data = request.get_json()
    if not data or "name" not in data:
        return error_response("Missing required field: name", 400)

    new_skill = Skill(name=data["name"], level=data.get("level", 1))
    db.session.add(new_skill)
    db.session.commit()
    return success_response({"message": "Skill created successfully", "id": new_skill.id}, 201)


@api_bp.route('/skills/<int:skill_id>', methods=['PUT'])
@admin_required
def update_skill(skill_id):
    """Update a skill (admin only)."""
    skill = db.session.get(Skill, skill_id)
    if not skill:
        return error_response("Skill not found", 404)

    data = request.get_json()
    if not data:
        return error_response("No data provided", 400)

    skill.name = data.get("name", skill.name)
    skill.level = data.get("level", skill.level)
    db.session.commit()
    return success_response({"message": "Skill updated successfully", "skill": skill.to_dict()})


@api_bp.route('/skills/<int:skill_id>', methods=['DELETE'])
@admin_required
def delete_skill(skill_id):
    """Delete a skill (admin only)."""
    skill = db.session.get(Skill, skill_id)
    if not skill:
        return error_response("Skill not found", 404)

    db.session.delete(skill)
    db.session.commit()
    return success_response({"message": "Skill deleted successfully"})

# =====================================================
# PLAYER PROGRESS
# =====================================================


@api_bp.route('/progress/<int:player_id>', methods=['GET'])
@jwt_required()
def get_player_progress(player_id):
    """Get a player's progress summary."""
    player = db.session.get(Player, player_id)
    if not player:
        return error_response("Player not found", 404)

    total_quests = len(player.quests)
    total_xp = sum(q.xp for q in player.quests)

    data = {
        "player_name": player.name,
        "total_quests_completed": total_quests,
        "total_xp_gained": total_xp,
        "level": player.level
    }
    return success_response(data)
