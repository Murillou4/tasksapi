from marshmallow import Schema, fields, ValidationError
from PIL import Image
import io

class UserSchema(Schema):
    name = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class TaskSchema(Schema):
    topic = fields.Str(required=True, validate=lambda x: 3 <= len(x) <= 200)
    completed = fields.Bool()

class PhotoValidator:
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_FORMATS = {'PNG', 'JPEG', 'JPG'}
    MAX_DIMENSIONS = (2000, 2000)

    @staticmethod
    def validate_photo(photo_bytes):
        # Validar tamanho
        if len(photo_bytes) > PhotoValidator.MAX_FILE_SIZE:
            raise ValidationError("Tamanho da foto excede 5MB")

        try:
            # Validar formato e dimensões
            img = Image.open(io.BytesIO(photo_bytes))
            
            if img.format not in PhotoValidator.ALLOWED_FORMATS:
                raise ValidationError("Formato de imagem não permitido")

            if img.size[0] > PhotoValidator.MAX_DIMENSIONS[0] or img.size[1] > PhotoValidator.MAX_DIMENSIONS[1]:
                raise ValidationError("Dimensões da imagem excedem o limite máximo")

            # Converter para RGB se necessário e otimizar
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Otimizar e redimensionar se necessário
            output = io.BytesIO()
            img.save(output, format='JPEG', optimize=True, quality=85)
            return output.getvalue()

        except Exception as e:
            raise ValidationError(f"Erro ao processar imagem: {str(e)}")