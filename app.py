from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def calcular_emprestimo(renda, valor, prazo, taxa):
    try:
        renda_mensal = float(renda)
        valor_emprestimo = float(valor)
        prazo_meses = int(prazo)
        if taxa:
            taxa_juros_anual = float(taxa)
        else:
            taxa_juros_anual = 0.06  # Taxa de juros anual de 6% (valor fictício)

        taxa_juros_mensal = taxa_juros_anual / 12  # Convertendo taxa anual para mensal
        prestacao_mensal = (taxa_juros_mensal * valor_emprestimo) / (1 - (1 + taxa_juros_mensal) ** -prazo_meses)
        custo_total = prestacao_mensal * prazo_meses

        return {
            "prestacao": round(prestacao_mensal, 2),
            "custo_total": round(custo_total, 2)
        }
    except ValueError:
        return {"error": "Por favor, insira valores numéricos válidos para a renda, empréstimo e prazo."}


@app.route('/calcular_emprestimo', methods=['POST'])
def calcular():
    renda = request.form['renda']
    valor = request.form['valor']
    prazo = request.form['prazo']
    taxa = request.form['taxa']

    resultado = calcular_emprestimo(renda, valor, prazo, taxa)

    return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)


