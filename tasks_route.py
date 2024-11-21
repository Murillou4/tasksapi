from flask import request, jsonify
from flask_app import app
from flask_app import db
from datetime import datetime
from auth_middleware import require_auth
from log_service import LogService
from limiter_service import limiter
from schemas import TaskSchema
from marshmallow import ValidationError

@limiter.limit("50 per minute")
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
        LogService.error(f'Error on get tasks by user route: {e}')
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
@limiter.limit("20 per minute; 200 per hour")
@app.route('/tasks/add', methods=['POST'])
@require_auth
def add_task():
    try:
        # Validar dados de entrada
        schema = TaskSchema()
        data = schema.load(request.json)
        
        # Criar tarefa
        iso_date = datetime.now().isoformat()
        db.add_task(data['topic'], iso_date, request.uid)
        
        return jsonify({
            'message': 'Task added successfully',
            'task': {
                'id': db.cur.lastrowid,
                'topic': data['topic'],
                'created_at': iso_date,
                'completed': False
            }
        }), 200
        
    except ValidationError as e:
        return jsonify({'message': 'Invalid data', 'errors': e.messages}), 400
    except Exception as e:
        LogService.error(f'Error on add task route: {e}')
        return jsonify({'message': 'Internal server error'}), 500
    
@limiter.limit("30 per minute; 300 per hour")
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
        LogService.error(f'Error on update task topic route: {e}')
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
        LogService.error(f'Error on update task completed route: {e}')
        return jsonify({'message': 'Internal server error'}), 500