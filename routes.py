from flask import render_template, request, redirect, url_for, session, g
from .models import Cliente  # Importando o modelo Cliente
from .functions import cadastrar_cliente, atualizar_cliente, listar_clientes, pesquisar_placa, excluir_cliente

# Função que registra as rotas no app
def init_routes(app):

    @app.before_request
    def before_request():
        # Define o tema como 'dark' por padrão, caso não esteja na sessão
        g.tema = session.get('tema', 'dark')  # 'g' é usado para armazenar variáveis globais por requisição

    @app.route('/cadastro', methods=['POST', 'GET'])
    def cadastrar():
        if request.method == 'POST':
            nome = request.form['nometxt'].strip()
            tell = request.form['telltxt'].strip()
            placa = request.form['placatxt'].strip().lower()
            carro = request.form['carrotxt'].strip()
            info = request.form['infotxt'].strip()
            if cadastrar_cliente(placa, nome, tell, carro, info):
                session['mensagem'] = 'Informações salvas'
                session['cor'] = '#0f8100'
            else:
                session['mensagem'] = 'Não cadastrado, houve um erro'
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
            if atualizar_cliente(idd, placa, nome, tell, carro, info):
                session['mensagem'] = f'Cadastro da placa {placa} atualizado'
                session['cor'] = '#0f8100'
            else:
                session['mensagem'] = 'Não cadastrado, ouve um erro'
                session['cor'] = '#ff2222'

        return redirect(url_for('home'))

    @app.route('/excluir', methods=['POST', 'GET'])
    def excluir():
        idd = request.form['id']
        excluir_cliente(idd)
        return redirect(url_for('home'))

    @app.route('/pesquisar', methods=['POST', 'GET'])
    def pesquisar():
        if request.method == 'POST' and request.form.get('placaPesquisa'):
            info = request.form['placaPesquisa'].strip()
            tipo = request.form['tipoPesquisa']
        clientes = pesquisar_placa(info, tipo)
        return render_template('lista.html', clientes=clientes, info=info, tipo=tipo, tema=g.tema)

    @app.route('/pesq/<placa>', methods=['POST', 'GET'])
    def link(placa):
        casos = pesquisar_placa(placa, 'placa')
        return render_template('pesquisa.html', casos=casos, placa=placa, tema=g.tema)

    @app.route('/listar', methods=['POST', 'GET'])
    def listar():
        return render_template('lista.html', clientes=listar_clientes(), tema =g.tema)

    @app.route('/editar', methods=['POST', 'GET'])
    def edita():
        info = request.form['id']
        casos = pesquisar_placa(info, 'id')
        return render_template('edicao.html', casos=casos[0], tema=g.tema)
    
    @app.route('/trocar-tema', methods=['POST'])
    def trocar_tema():
        tema_atual = session.get('tema', 'dark')
        novo_tema = 'dark' if tema_atual == 'light' else 'light'
        session['tema'] = novo_tema
        return redirect(url_for('home'))

    @app.route('/')
    def home():
        mensagem = session.pop('mensagem', '')
        cor = session.pop('cor', '#17181d')
        return render_template('cadastro.html', mensagem=mensagem, cor=cor, tema=g.tema)
