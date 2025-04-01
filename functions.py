from .models import Cliente
from . import db
from datetime import datetime


def cadastrar_cliente(placa, nome, tell, carro, info):
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    novo_cliente = Cliente(placa=placa, nome=nome, tell=tell, carro=carro, info=info, data=data_atual)
    try:
        db.session.add(novo_cliente)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar cliente: {e}")
        return False


def atualizar_cliente(id, placa, nome, tell, carro, info):
    cliente = Cliente.query.get(id)
    if cliente:
        cliente.placa = placa
        cliente.nome = nome
        cliente.tell = tell
        cliente.carro = carro
        cliente.info = info
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar cliente: {e}")
            return False
    return False


def excluir_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        try:
            db.session.delete(cliente)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao excluir cliente: {e}")
            return False
    return False


def listar_clientes():
    return Cliente.query.all()


def pesquisar_placa(info, tipo):
    try:
        # Verifica o tipo de filtro
        if tipo == 'id':
            resultados = Cliente.query.filter_by(id=info).all()  #Busca exata por ID
        elif tipo in ['placa', 'nome', 'carro']:
            # Busca com filtro LIKE para os outros tipos
            filtro = {tipo: f"%{info}%"}
            resultados = Cliente.query.filter(getattr(Cliente, tipo).like(filtro[tipo])).all()
        else:
            raise ValueError("Tipo de pesquisa inválido")
        return resultados
    except Exception as erro:
        print(f"Erro ao pesquisar: {erro}")
        return []
