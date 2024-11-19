from flask import request, jsonify
from jwt_service import JWTService
from flask_app import app
from flask_app import db
from datetime import datetime
from auth_middleware import require_auth


@app.route('/tasks/byuser', methods=['GET'])
@require_auth
def get_tasks_by_user():
    try:
        tasks_raw = db.get_tasks(request.uid)
        tasks = []
        for task in tasks_raw:
            tasks.append({'id': task[0], 'topic': task[1], 'created_at': task[2], 'completed': task[3]})
        return jsonify({'message': 'Tasks fetched successfully', 'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500


"""
Adiciona uma nova tarefa para o usuário autenticado.

Método: POST
Endpoint: /tasks/add

Parâmetros JSON:
    - topic (str): O tópico ou título da tarefa.

Retorna:
    JSON:
        - message (str): Mensagem de sucesso ou erro.
        - task (dict, opcional): Detalhes da tarefa adicionada.
"""

@app.route('/tasks/add', methods=['POST'])
@require_auth
def add_task():

    data = request.json

    if not data['topic']:
        return jsonify({'message': 'Topic is required'}), 400
    
    try:
        iso_date = datetime.now().isoformat()
        db.add_task(data['topic'], iso_date, request.uid)
        return jsonify({'message': 'Task added successfully', 'task': {'id': db.cur.lastrowid, 'topic': data['topic'], 'created_at': iso_date, 'completed': False}}), 200
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500
    

@app.route('/tasks/update/topic', methods=['PUT'])
@require_auth
def update_task_topic():    
    data = request.json

    if not data['id']:
        return jsonify({'message': 'Id is required'}), 400
    
    if not data['topic']:
        return jsonify({'message': 'Topic is required'}), 400
    
    try:
        #Obtém a tarefa da base de dados e verifica se existe
        task_raw = db.get_task(data['id'])
        if not task_raw:
            return jsonify({'message': 'Task not found'}), 404
        #Verifica se o usuário é o dono da tarefa
        if task_raw[4] != request.uid:
            return jsonify({'message': 'You are not the owner of this task'}), 403
        #Atualiza o tópico da tarefa
        db.update_task_topic(data['id'], data['topic'])
        return jsonify({'message': 'Task updated successfully', 'task': {'id': data['id'], 'topic': data['topic'], 'created_at': task_raw[2], 'completed': task_raw[3]}}), 200
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500
    
    
    
@app.route('/tasks/update/completed', methods=['PUT'])
@require_auth
def update_task_completed():
    data = request.json

    if not data['id']:
        return jsonify({'message': 'Id is required'}), 400
    
    if not data['completed']:
        return jsonify({'message': 'Completed is required'}), 400
    
    try:
        #Obtém a tarefa da base de dados e verifica se existe
        task_raw = db.get_task(data['id'])
        if not task_raw:
            return jsonify({'message': 'Task not found'}), 404
        #Verifica se o usuário é o dono da tarefa
        if task_raw[4] != request.uid:
            return jsonify({'message': 'You are not the owner of this task'}), 403
        #Atualiza o tópico da tarefa
        db.update_task_completed(data['id'], data['completed'])
        return jsonify({'message': 'Task updated successfully', 'task': {'id': data['id'], 'topic': task_raw[1], 'created_at': task_raw[2], 'completed': data['completed']}}), 200
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500