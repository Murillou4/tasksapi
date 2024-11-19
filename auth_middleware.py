from functools import wraps
from flask import request, jsonify
from jwt_service import JWTService

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is required'}), 401
            
        try:
            token = token.split(" ")[1]
            payload = JWTService.verify_user_token(token)
            if not payload['uid']:
                return jsonify({'message': 'Please return to login'}), 401
            request.uid = payload['uid']
            return f(*args, **kwargs)
        except Exception:
            return jsonify({'message': 'Invalid token'}), 401
            
    return decorated 