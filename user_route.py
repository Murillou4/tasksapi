from flask import request, jsonify
from flask_app import app
from flask_app import db
import base64
from auth_middleware import require_auth
from log_service import LogService
from limiter_service import limiter
from schemas import PhotoValidator
from marshmallow import ValidationError
'''
    Endpoint para obter informações do usuário autenticado.

    Esta função é responsável por validar o token de autenticação fornecido
    no cabeçalho da requisição e, se o token for válido, retornar as informações
    do usuário associadas ao uid contido no token.

    Returns:
        json: Dicionário com as informações do usuário ou mensagem de erro
'''
@limiter.limit("30 per minute")
@app.route('/user/me', methods=['GET'])
@require_auth
def me():
    try:
        #Obtém o usuário da base de dados
        try:
            user = db.get_user(request.uid)
            if not user:
                return jsonify({'message': 'User not found'}), 404
        except Exception as e:
            return jsonify({'message': 'Internal server error'}), 500
        photo_base64 = None
        if user[4]:
            photo_base64 = base64.b64encode(user[4]).decode('utf-8')
        return jsonify({'name': user[1], 'email': user[2], 'photo': photo_base64}), 200
    except Exception as e:
        LogService.error(f'Error on me route: {e}')
        return jsonify({'message': 'Internal server error'}), 500
    
@limiter.limit("10 per minute; 100 per hour")
@app.route('/user/update/photo', methods=['PUT'])
@require_auth
def update_photo():
    if not request.files.get('photo'):
        return jsonify({'message': 'Photo is required'}), 400
    
    try:
        photo = request.files.get('photo')
        photo_bytes = photo.read()
        
        # Validar e otimizar a foto
        processed_photo = PhotoValidator.validate_photo(photo_bytes)
        
        # Salvar foto processada
        db.update_user_photo(request.uid, processed_photo)
        
        # Retornar foto processada
        photo_base64 = base64.b64encode(processed_photo).decode('utf-8')
        return jsonify({
            'message': 'Photo updated successfully',
            'photo': photo_base64
        }), 200
        
    except ValidationError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        LogService.error(f'Error on update photo route: {e}')
        return jsonify({'message': 'Internal server error'}), 500
    

@limiter.limit("10 per minute; 100 per hour")
@app.route('/user/delete', methods=['DELETE'])
@require_auth
def delete_user():
    try:
        user = db.get_user(request.uid)
        if not user:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        LogService.error(f'Error on delete user route: {e}')
        return jsonify({'message': 'Internal server error'}), 500
    
    try:
        db.delete_user(request.uid)
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        LogService.error(f'Error on delete user route: {e}')
        return jsonify({'message': 'Internal server error'}), 500

    

