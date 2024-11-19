import jwt

class JWTService:
    @staticmethod
    def generate_user_token(payload: dict) -> str:
        return jwt.encode(payload, '9b07fef5-493e-4b95-816e-598159db70c3', algorithm='HS256')
    
    @staticmethod
    def verify_user_token(token: str) -> dict:
        return jwt.decode(token, '9b07fef5-493e-4b95-816e-598159db70c3', algorithms=['HS256'])

