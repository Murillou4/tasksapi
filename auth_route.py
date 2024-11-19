#A pasta não está no mesmo nível da pasta routes
from flask import request, jsonify
from jwt_service import JWTService
from email_validator import validate_email, EmailNotValidError
from password_service import PasswordService
from flask_app import app
from flask_app import db
import uuid


'''
    Rota para login do usuário

    Essa rota é responsável por realizar o login do usuário, recebendo como parâmetro
    o email e a senha do mesmo. O email é verificado se é válido, se o usuário existe
    e se a senha informada é válida. Se todas as condições forem verdadeiras, um token
    é gerado com o uid do usuário e retorna o status 200 com o token. Caso contrário,
    retorna um erro com o status apropriado.

    Parameters:
        email (str): Email do usuário
        password (str): Senha do usuário

    Returns:
        json: Dicionário com o token do usuário
'''
@app.route('/auth/login', methods=['POST'])
def login():

    
    data = request.json
    email = data.get('email')
    password = data.get('password')
    #Verifica se o email foi informado 
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    #Verifica se a senha foi informada
    if not password:
        return jsonify({'message': 'Password is required'}), 400
    # UID, name, email, password, photo
    try:
        #Verifica se o usuário existe
        user: tuple = db.get_user_by_email(email)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        #Verifica se a senha é válida
        if not PasswordService.verify_password(password, user[3]):
            return jsonify({'message': 'Invalid password'}), 401
    #Caso ocorra um erro interno
    except Exception as e:
        return jsonify({'message': f'Internal server error {e}'}), 500
    
    #Gera o token do usuário com o payload contendo o uid
    payload = {'uid': user[0]}
    token = JWTService.generate_user_token(payload)
    
    return jsonify({'message': 'Login successful', 'token': token}), 200


'''
    Rota para registro de um novo usuário

    Essa rota é responsável por registrar um novo usuário, recebendo como parâmetro
    o email e a senha do mesmo. O email é validado e verificado se já existe na base
    de dados. Se o email for válido e não estiver em uso, e a senha cumprir os requisitos,
    o usuário é criado na base de dados. Após a criação do usuário, um token é gerado
    com o uid do usuário e retorna o status 200 com o token. Caso contrário, retorna
    um erro com o status apropriado.

    Parameters:
        email (str): Email do usuário
        password (str): Senha do usuário

    Returns:
        json: Dicionário com o token do usuário ou mensagem de erro
'''
@app.route('/auth/register', methods=['POST'])
def register():

    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name:
        return jsonify({'message': 'Name is required'}), 400
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    if not password:
        return jsonify({'message': 'Password is required'}), 400
    
    #verifique se o email já existe na base de dados
    if db.get_user_by_email(email):
        return jsonify({'message': 'Email already exists'}), 400
    #Verifica se o email é válido
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return jsonify({'message': 'Invalid email'}), 400
    #Verifica se a senha é válida
    if not PasswordService.is_password_valid(password):
        return jsonify({'message': 'Invalid password'}), 400
    #Gera o hash da senha
    hashed_password = PasswordService.hash_password(password)
    #Gera o uid do usuário
    uid = str(uuid.uuid4())
    
    #Cria o usuário na base de dados
    try:
        db.create_user(uid,name,email, hashed_password,None)
    except Exception as e:
        return jsonify({'message': f'Failed to create user {e}'}), 400
    
    #Verifica se o usuário foi criado com sucesso
    try:
        user = db.get_user_by_email(email)
        if not user:
            return jsonify({'message': 'Failed to create user'}), 400
        #Gera o token do usuário com o payload contendo o uid
        payload = {'uid': user.uid}
        token = JWTService.generate_user_token(payload)
        
        return jsonify({'message': 'Register successful', 'token': token}), 200

    except Exception as e:
        return jsonify({'message': f'Internal server error {e}'}), 500

