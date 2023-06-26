from flask import Flask, request, render_template, session, url_for, redirect
from funcoes import *

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'


@app.route('/cadastro', methods=['POST', 'GET'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nometxt'].strip()
        tell = request.form['telltxt'].strip()
        placa = request.form['placatxt'].strip().lower()
        carro = request.form['carrotxt'].strip()
        info = request.form['infotxt'].strip()
        if cadastrarBanco(placa, nome, tell, carro, info):
            session['mensagem'] = 'Informações salvas'
            session['cor'] = '#0f8100'
        else:
            session['mensagem'] = 'Não cadastrado, ouve um erro'
            session['cor'] = '#ff2222'

    return redirect(url_for('home'))


@app.route('/atualizar', methods=['POST', 'GET'])
def atualizar():
    if request.method == 'POST':
        idd = request.form['id']
        nome = request.form['nometxt'].strip()
        tell = request.form['telltxt'].strip()
        placa = request.form['placatxt'].strip().lower()
        carro = request.form['carrotxt'].strip()
        info = request.form['infotxt'].strip()
        if atualizarBanco(idd, placa, nome, tell, carro, info):
            session['mensagem'] = f'Cadastro da placa {placa} atualizado'
            session['cor'] = '#0f8100'
        else:
            session['mensagem'] = 'Não cadastrado, ouve um erro'
            session['cor'] = '#ff2222'

    return redirect(url_for('home'))


@app.route('/excluir', methods=['POST', 'GET'])
def excluir():
    idd = request.form['id']
    excluir_dado(idd)
    return redirect(url_for('home'))


@app.route('/pesquisar', methods=['POST', 'GET'])
def pesquisar():
    if request.method == 'POST' and request.form.get('placaPesquisa'):
        info = request.form['placaPesquisa'].strip()
        tipo = request.form['tipoPesquisa']
    clientes = pesquisar_placa(info, tipo)
    return render_template('lista.html', clientes=clientes, info=info, tipo=tipo, tema=pegar_tema())


@app.route('/pesq/<placa>', methods=['POST', 'GET'])
def link(placa):
    casos = pesquisar_placa(placa, 'placa')
    return render_template('pesquisa.html', casos=casos, placa=placa, tema=pegar_tema())


@app.route('/listar', methods=['POST', 'GET'])
def listar():
    return render_template('lista.html', tema=pegar_tema(), clientes=listar_dados())


@app.route('/editar', methods=['POST', 'GET'])
def edita():
    if request.method == 'POST':
        info = request.form['id']
        casos = pesquisar_placa(info, 'id')
    return render_template('edicao.html', tema=pegar_tema(), casos=casos)


@app.route('/alterar-tema', methods=['POST', 'GET'])
def tema():
    novo_tema = 'light' if pegar_tema() == 'dark' else 'dark'
    with open('config.txt', 'w') as arquivo:
        arquivo.write(novo_tema)
    return redirect(url_for('home'))


@app.route('/')
def home():
    mensagem = session.pop('mensagem', '')
    cor = session.pop('cor', '#17181d')
    with open('config.txt', 'r') as arquivo:
        temaa = arquivo.read().strip()
    return render_template('cadastro.html', mensagem=mensagem, cor=cor, tema=temaa)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
