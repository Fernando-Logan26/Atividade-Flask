from flask import Flask, render_template

app_Fernando = Flask(__name__)

# Dados do catálogo NOKIS
PRODUTOS = [
    {
        "id": 1,
        "nome": "Camiseta Oversized Blank",
        "preco": "R$ 119,90",
        "descricao": "Algodão 100% de alta gramatura com modelagem ampla e minimalista."
    },
    {
        "id": 2,
        "nome": "Moletom Monochrome Heavy",
        "preco": "R$ 289,90",
        "descricao": "Interior flanelado, capuz duplo estruturado e acabamento premium."
    },
    {
        "id": 3,
        "nome": "Calça Jogger Tech",
        "preco": "R$ 199,90",
        "descricao": "Corte moderno em tecido técnico respirável com bolsos utilitários."
    },
    {
        "id": 4,
        "nome": "Jaqueta Windbreaker NOKIS",
        "preco": "R$ 349,90",
        "descricao": "Corta-vento impermeável em tom preto fosco de alto contraste."
    }
]

@app_Fernando.route('/')
def index():
    return render_template('index.html')

@app_Fernando.route('/produtos')
def produtos():
    return render_template('produtos.html', lista_produtos=PRODUTOS)

@app_Fernando.route('/contato')
def contato():
    return render_template('contato.html')

@app_Fernando.route('/login')
def login():
    return render_template('login.html')

@app_Fernando.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

if __name__ == '__main__':
    app_Fernando.run(debug=True, port=8000)