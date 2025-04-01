from . import db

class Cliente(db.Model):
    __tablename__ = 'Clientes'

    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    tell = db.Column(db.String(50), nullable=False)
    carro = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(255))
    data = db.Column(db.String(50), nullable=False)

    def __init__(self, placa, nome, tell, carro, info, data):
        self.placa = placa
        self.nome = nome
        self.tell = tell
        self.carro = carro
        self.info = info
        self.data = data

    def __repr__(self):
        return f"<Cliente {self.placa}, {self.nome}>"
