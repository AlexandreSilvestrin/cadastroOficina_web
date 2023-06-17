from flask import Flask, request, render_template, session, url_for, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'


def cadastrarBanco(placa, nome, tell, carro, info):
    banco = sqlite3.connect('clientes.db')
    cursor = banco.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            placa TEXT primary key,
            nome TEXT,
            tell TEXT,
            carro TEXT,
            info TEXT
        )
    ''')
    try:
        cursor.execute(f'''INSERT INTO clientes VALUES ('{placa}','{nome}','{tell}','{carro}','{info}')''')
    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ", erro)
        if str(erro) == 'UNIQUE constraint failed: clientes.placa':
            banco.close()
            return False
    else:
        banco.commit()
        banco.close()
        return True


@app.route('/cadastro', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print('entrou no if')
        nome = request.form['nometxt'].strip()
        tell = request.form['telltxt'].strip()
        placa = request.form['placatxt'].strip()
        carro = request.form['carrotxt'].strip()
        info = request.form['infotxt'].strip()
        if not nome or not tell or not placa or not carro or not info:
            session['mensagem'] = 'Preencha todos os campos'
            session['cor'] = '#ff2222'
        elif cadastrarBanco(placa, nome, tell, carro, info):
            session['mensagem'] = 'Usuário cadastrado'
            session['cor'] = '#0f8100'
        else:
            session['mensagem'] = 'Não cadastrado, cliente já possui cadastro'
            session['cor'] = '#ff2222'

    return redirect(url_for('home'))


@app.route('/')
def home():
    mensagem = session.pop('mensagem', '')
    cor = session.pop('cor', '#17181d')
    return render_template('cadastro.html', mensagem=mensagem, cor=cor)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
