import re
from flask import Flask, render_template, request, redirect, url_for, flash, session

app_Fernando = Flask(__name__)
app_Fernando.secret_key = 'nokis_chave_secreta'

# Catálogo fixo de produtos com imagens .jpeg
PRODUTOS = [
    {
        "id": 1,
        "nome": "Camiseta Oversized Blank",
        "preco": "R$ 119,90",
        "descricao": "Algodão 100% de alta gramatura com modelagem ampla e minimalista.",
        "imagem": "img/produto1.jpeg"
    },
    {
        "id": 2,
        "nome": "Moletom Monochrome Heavy",
        "preco": "R$ 289,90",
        "descricao": "Interior flanelado, capuz duplo estruturado e acabamento premium.",
        "imagem": "img/produto2.jpeg"
    },
    {
        "id": 3,
        "nome": "Calça Jogger Tech",
        "preco": "R$ 199,90",
        "descricao": "Corte moderno em tecido técnico respirável com bolsos utilitários.",
        "imagem": "img/produto3.jpeg"
    },
    {
        "id": 4,
        "nome": "Jaqueta Windbreaker NOKIS",
        "preco": "R$ 349,90",
        "descricao": "Corta-vento impermeável em tom preto fosco de alto contraste.",
        "imagem": "img/produto4.jpeg"
    }
]

# Base de dados simulada para armazenar novos cadastros
USUARIOS_CADASTRADOS = {}

def validar_senha_alfanumerica(senha):
    """Retorna True se a senha tiver pelo menos uma letra e pelo menos um número."""
    tem_letra = bool(re.search(r'[a-zA-Z]', senha))
    tem_numero = bool(re.search(r'\d', senha))
    return tem_letra and tem_numero

@app_Fernando.route('/')
def index():
    return render_template('index.html')

@app_Fernando.route('/produtos')
def produtos():
    return render_template('produtos.html', lista_produtos=PRODUTOS)

@app_Fernando.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form.get('nome')
        flash(f'Obrigado pela mensagem, {nome}! Entraremos em contato em breve.', 'sucesso')
        return redirect(url_for('contato'))
    return render_template('contato.html')

@app_Fernando.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')

        # 1. Login do Administrador (E-mail: admin@nokis.com | Senha: 1234)
        if email == 'admin@nokis.com' and senha == '1234':
            session['usuario'] = {
                'nome': 'Administrador NOKIS',
                'email': 'admin@nokis.com',
                'tipo': 'admin',
                'status': 'Acesso Total (Admin)',
                'preferencia': 'Gestão de Catálogo'
            }
            flash('Sessão iniciada como Administrador!', 'sucesso')
            return redirect(url_for('usuario'))

        # 2. Login do Usuário Padrão (E-mail: user@nokis.com | Senha: nokis456)
        elif email == 'user@nokis.com' and senha == 'nokis456':
            session['usuario'] = {
                'nome': 'NOKIS Member',
                'email': 'user@nokis.com',
                'tipo': 'cliente',
                'status': 'Membro Oficial',
                'preferencia': 'Streetwear Monocromático'
            }
            flash('Bem-vindo(a) de volta, NOKIS Member!', 'sucesso')
            return redirect(url_for('usuario'))

        # 3. Login de utilizadores cadastrados no formulário
        elif email in USUARIOS_CADASTRADOS and USUARIOS_CADASTRADOS[email]['senha'] == senha:
            usuario_data = USUARIOS_CADASTRADOS[email]
            session['usuario'] = {
                'nome': usuario_data['nome'],
                'email': email,
                'tipo': 'cliente',
                'status': 'Membro Cadastrado',
                'preferencia': 'Streetwear Monocromático'
            }
            flash(f'Bem-vindo(a) de volta, {usuario_data["nome"]}!', 'sucesso')
            return redirect(url_for('usuario'))

        # Caso as credenciais estejam incorretas
        else:
            flash('E-mail ou senha incorretos!', 'erro')
            return redirect(url_for('login'))

    return render_template('login.html')

@app_Fernando.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')

        if not nome or not email or not senha:
            flash('Preencha todos os campos para se cadastrar.', 'erro')
            return redirect(url_for('cadastro'))

        # Validação alfanumérica para novos cadastros de usuários
        if not validar_senha_alfanumerica(senha):
            flash('A senha deve conter pelo menos uma letra e um número!', 'erro')
            return redirect(url_for('cadastro'))

        # Salva o usuário no dicionário de cadastros
        USUARIOS_CADASTRADOS[email] = {
            'nome': nome,
            'senha': senha
        }

        # Cria a sessão imediatamente após o cadastro
        session['usuario'] = {
            'nome': nome,
            'email': email,
            'tipo': 'cliente',
            'status': 'Novo Membro',
            'preferencia': 'Streetwear Monocromático'
        }
        flash(f'Conta criada com sucesso para {nome}!', 'sucesso')
        return redirect(url_for('usuario'))

    return render_template('cadastro.html')

@app_Fernando.route('/usuario')
def usuario():
    dados_usuario = session.get('usuario')
    if not dados_usuario:
        flash('Faça login ou cadastre-se para acessar o perfil.', 'erro')
        return redirect(url_for('login'))
    return render_template('usuario.html', usuario=dados_usuario)

@app_Fernando.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sessão encerrada.', 'sucesso')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app_Fernando.run(debug=True, port=8000)