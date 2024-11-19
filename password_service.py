from bcrypt import hashpw, gensalt, checkpw
import re

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
        if len(password) < 8:
            return False
        
        # Pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', password):
            return False
            
        # Pelo menos um número
        if not re.search(r'\d', password):
            return False
            
        # Pelo menos um caractere especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
            
        return True
