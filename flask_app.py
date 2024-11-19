from flask import Flask
from database_service import DatabaseService
db = DatabaseService()
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Importando as rotas
from auth_route import *
from user_route import *
from tasks_route import *

if __name__ == '__main__':
    app.run(debug=True)
