from flask import request, jsonify
from jwt_service import JWTService
from flask_app import app
from flask_app import db
from datetime import datetime

@app.route('/tasks/byuser', methods=['GET'])
def get_tasks_by_user():
    token = request.headers.get('Authorization')
    #Verifica se o token foi informado
    if not token:
        return jsonify({'message': 'Token is required'}), 400
    
    #Verifica se o token é válido
    verified_token = None
    try:
        token = token.split(" ")[1]
        verified_token = JWTService.verify_user_token(token)
    except Exception as e:
        return jsonify({'message': f'Invalid token {e}'}), 401

    if not verified_token:
        return jsonify({'message': 'Invalid token'}), 401
    
    #Obtém o uid do token
    uid = verified_token['uid']

    try:
        tasks_raw = db.get_tasks(uid)
        tasks = []
        for task in tasks_raw:
            tasks.append({'id': task[0], 'topic': task[1], 'created_at': task[2], 'completed': task[3]})
        return jsonify({'message': 'Tasks fetched successfully', 'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'message': f'Internal server error {e}'}), 500

@app.route('/tasks/add', methods=['POST'])
def add_task():
    token = request.headers.get('Authorization')
    #Verifica se o token foi informado
    if not token:
        return jsonify({'message': 'Token is required'}), 400
    
    #Verifica se o token é válido
    verified_token = None
    try:
        token = token.split(" ")[1]
        verified_token = JWTService.verify_user_token(token)
    except Exception as e:
        return jsonify({'message': f'Invalid token {e}'}), 401

    if not verified_token:
        return jsonify({'message': 'Invalid token'}), 401
    
    #Obtém o uid do token
    uid = verified_token['uid']

    data = request.json

    if not data['topic']:
        return jsonify({'message': 'Topic is required'}), 400
    
    try:
        iso_date = datetime.now().isoformat()
        db.add_task(data['topic'], iso_date, uid)
        return jsonify({'message': 'Task added successfully', 'task': {'id': db.cur.lastrowid, 'topic': data['topic'], 'created_at': iso_date, 'completed': False}}), 200
    except Exception as e:
        return jsonify({'message': f'Internal server error {e}'}), 500
    

@app.route('/tasks/update', methods=['PUT'])
def update_task():
    token = request.headers.get('Authorization')
    #Verifica se o token foi informado
    if not token:
        return jsonify({'message': 'Token is required'}), 400
    
    #Verifica se o token é válido
    verified_token = None
    try:
        token = token.split(" ")[1]
        verified_token = JWTService.verify_user_token(token)
    except Exception as e:
        return jsonify({'message': f'Invalid token {e}'}), 401

    if not verified_token:
        return jsonify({'message': 'Invalid token'}), 401
    
    #Obtém o uid do token
    uid = verified_token['uid']

    data = request.json

    if not data['id']:
        return jsonify({'message': 'Id is required'}), 400
    
    if not data['topic']:
        return jsonify({'message': 'Topic is required'}), 400
    
    
    
