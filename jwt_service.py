import jwt
import os
class JWTService:
    @staticmethod
    def generate_user_token(payload: dict) -> str:
        secret_key = os.getenv('FLASK_SECRET_KEY')
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    @staticmethod
    def verify_user_token(token: str) -> dict:
        secret_key = os.getenv('FLASK_SECRET_KEY')
        return jwt.decode(token, secret_key, algorithms=['HS256'])

