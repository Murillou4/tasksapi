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

# Importando as rotas
from auth_route import *
from user_route import *
from tasks_route import *

"""
    Handles 429 error and logs it in the structured log service.

    Args:
        e (Exception): The exception that triggered the 429 error.

    Returns:
        A response with a JSON object containing a message and the error description.
        The status code is 429.
"""
@app.errorhandler(429)
def ratelimit_handler(e):

    LogService.rate_limit_exceeded(request.path, str(e.description))
    return jsonify({
        "message": "Too many requests. Please try again later.",
        "error": str(e.description)
    }), 429



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  


