from flask import Flask
from database_service import DatabaseService
db = DatabaseService()
app = Flask(__name__)

# Importando as rotas
from auth_route import *
from user_route import *
from tasks_route import *

print(db.get_tasks('b900a03f-395f-461a-b0e0-b8b9949cc486'))

if __name__ == '__main__':
    app.run(debug=True)
