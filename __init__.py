from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Se estiver usando config.py

    # Defina a chave secreta diretamente se não usar o config.py
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Defina sua chave secreta aqui

    db.init_app(app)

    # Importando as rotas diretamente no lugar adequado
    from .routes import init_routes
    init_routes(app)

    with app.app_context():
        db.create_all()  # Cria as tabelas do banco

    return app
