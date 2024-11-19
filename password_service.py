from bcrypt import hashpw, gensalt, checkpw

class PasswordService:
    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Gera um hash seguro para a senha usando bcrypt
        """
        return hashpw(password.encode('utf-8'), gensalt())

    @staticmethod
    def verify_password(password: str, hashed: bytes) -> bool:
        """
        Verifica se a senha corresponde ao hash
        """
        return checkpw(password.encode('utf-8'), hashed)

    @staticmethod
    def is_password_valid(password: str) -> bool:
        """
        Verifica se a senha é válida
        """
        return len(password) >= 8
