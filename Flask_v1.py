from flask import Flask, render_template

app_Fernando = Flask(__name__)
app_Fernando.config['SECRET_KEY'] = "palavra-secreta-IFRO"

@app_Fernando.route('/')
def index():
    return render_template("index.html")

@app_Fernando.route('/contato')
def contato():
    return render_template("contato.html")

@app_Fernando.route('/cadastro')
def cadastro():
    return render_template("cadastro.html")

@app_Fernando.route('/login')
def login():
    return render_template("login.html")

@app_Fernando.route('/usuario')
def usuario():
    return render_template("usuario.html")

if __name__ == '__main__':
    app_Fernando.run(debug=True, port=8000)