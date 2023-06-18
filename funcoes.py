import sqlite3
import time


def data():
    ano, mes, dia, hora, minuto, f, g, h, i = time.localtime()
    dataa = f"{dia:02}/{mes:02}/{ano} {hora}:{minuto:02}"
    print(dataa)
    return dataa


def pegar_tema():
    with open('config.txt', 'r') as arquivo:
        tema_atual = arquivo.read().strip()
    return tema_atual


def listar_dados():
    try:
        banco = sqlite3.connect('clientes.db')
        cursor = banco.cursor()
        resultados = cursor.execute(f'''SELECT * from clientes''').fetchall()
        banco.close()
    except sqlite3.Error as erro:
        banco.close()
        print(erro)
    else:
        return resultados


def cadastrarBanco(placa, nome, tell, carro, info):
    try:
        banco = sqlite3.connect('clientes.db')
        cursor = banco.cursor()
        cursor.execute(
            f'''INSERT INTO clientes VALUES (NULL,'{placa}','{nome}','{tell}','{carro}','{info}', '{data()}')''')
    except sqlite3.Error as erro:
        print(erro)
        banco.close()
        return False
    else:
        banco.commit()
        banco.close()
        return True


def pesquisar_placa(placa):
    try:
        banco = sqlite3.connect('clientes.db')
        cursor = banco.cursor()
        resultados = cursor.execute(f'''SELECT * from clientes WHERE placa = '{placa}' ''').fetchall()
        banco.close()
    except sqlite3.Error as erro:
        banco.close()
        print(erro)
    else:
        if len(resultados) == 0:
            return True, resultados
        else:
            return False, resultados


def excluir_dado(idd):
    try:
        banco = sqlite3.connect('clientes.db')
        cursor = banco.cursor()
        cursor.execute(f'''DELETE FROM clientes WHERE id = "{idd}" ''')
        banco.commit()
        banco.close()
    except sqlite3.Error as erro:
        banco.close()
        print(erro)
    else:
        return True


banco = sqlite3.connect('clientes.db')
cursor = banco.cursor()
cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT,
            nome TEXT,
            tell TEXT,
            carro TEXT,
            info TEXT,
            data text
        )
    ''')
banco.close()