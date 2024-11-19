from flask import Flask
from database_service import DatabaseService
db = DatabaseService()
from flask_cors import CORS
from dotenv import load_dotenv
import os
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
CORS(app)

# Importando as rotas
from auth_route import *
from user_route import *
from tasks_route import *


