from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

from database_service import DatabaseService
db = DatabaseService()

app = Flask(__name__)
CORS(app)

@app.route('/')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    }), 200

@app.errorhandler(429)
def ratelimit_handler(e):

    LogService.rate_limit_exceeded(request.path, str(e.description))
    return jsonify({
        "message": "Too many requests. Please try again later.",
        "error": str(e.description)
    }), 429
# Importando as rotas
from auth_route import *
from user_route import *
from tasks_route import *





