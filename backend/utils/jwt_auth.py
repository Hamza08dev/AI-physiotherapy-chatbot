import jwt
import datetime
from flask import request, jsonify

SECRET_KEY = "your_secret_key"

def generate_token(user_id):
    """Generates a JWT token for user authentication."""
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    """Verifies and decodes the JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def token_required(f):
    """Decorator to check for a valid JWT token in protected routes."""
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        user_id = verify_token(token)
        if not user_id:
            return jsonify({"message": "Token is invalid or expired!"}), 401
        
        return f(user_id, *args, **kwargs)
    
    return decorated
