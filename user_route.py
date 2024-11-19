from flask import request, jsonify
from jwt_service import JWTService
from flask_app import app
from flask_app import db
import base64
from auth_middleware import require_auth
'''
    Endpoint para obter informações do usuário autenticado.

    Esta função é responsável por validar o token de autenticação fornecido
    no cabeçalho da requisição e, se o token for válido, retornar as informações
    do usuário associadas ao uid contido no token.

    Returns:
        json: Dicionário com as informações do usuário ou mensagem de erro
'''
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
        return jsonify({'message': 'Internal server error'}), 500
    

@app.route('/user/update/photo', methods=['PUT'])
@require_auth
def update_photo():
    if not request.files.get('photo'):
        return jsonify({'message': 'Photo is required'}), 400
    
    photo = None

    try:
        photo = request.files.get('photo')
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

    if not photo:
        return jsonify({'message': 'Photo is required'}), 400

    if photo.filename == '':
        return jsonify({'message': 'Photo is required'}), 400

    if not photo.filename.endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'message': 'Invalid photo format'}), 400
    
    try:
        photo_bytes = photo.read()
        db.update_user_photo(request.uid, photo_bytes)
        #Devolver também a foto atualizada
        photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
        return jsonify({'message': 'Photo updated successfully', 'photo': photo_base64}), 200
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500
    

    

