from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
        except Exception as e:
            return jsonify({"message": "Token is missing or invalid!", "error": str(e)}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated
