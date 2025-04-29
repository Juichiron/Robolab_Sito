from functools import wraps
import jwt
from flask import request, jsonify

SECRET_KEY = "your_secret_key"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token mancante!"}), 401
        try:
            decoded = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token scaduto!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token non valido!"}), 401
        return f(*args, **kwargs)
    return decorated