from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from backend.models import db, Player


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = db.session.get(Player, get_jwt_identity())
        if not user or not user.is_admin:
            return jsonify({"success": False, "error": "Admin privileges required"}), 403
        return fn(*args, **kwargs)
    return wrapper
