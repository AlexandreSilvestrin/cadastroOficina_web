from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/cadastro', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        nome = request.form['nometxt'].strip()
        tell = request.form['telltxt'].strip()
        placa = request.form['placatxt'].strip()
        carro = request.form['carrotxt'].strip()
        info = request.form['infotxt'].strip()

        if not any([nome, tell, placa, carro, info]):
            return """
                        <script>
                            alert('Por favor, preencha todos os campos!');
                            history.back();
                        </script>
                        """
        print(nome, tell, placa, carro, info)

    return render_template('cadastro.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
