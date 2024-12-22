# Importação de bibliotecas necessárias
import hashlib
import os
import time
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Configuração inicial do Flask
app = Flask(__name__)
app.secret_key = ''  # Chave secreta para sessões

# ============================
#  Funções auxiliares
# ============================

def get_db_connection():
    """
    Conecta ao banco de dados SQLite e retorna a conexão.
    """
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Retorna resultados como dicionários
    return conn

def generate_reset_token(user_id):
    """
    Gera um token único para recuperação de senha.
    """
    token = hashlib.sha256(f'{user_id}{time.time()}{os.urandom(24)}'.encode()).hexdigest()
    return token

def send_recovery_email(email, token):
    """
    Envia o e-mail de recuperação de senha usando a API do SendGrid.
    """
    from_email = Email("horrorbento@gmail.com")  # E-mail do remetente
    to_email = To(email)  # E-mail do destinatário
    subject = "Recuperação de Senha"
    recovery_link = f'http://localhost:5000/reset-password/{token}'  # Link para resetar senha

    content = Content("text/plain", f'Para redefinir sua senha, clique no link: {recovery_link}')
    mail = Mail(from_email, to_email, subject, content)

    try:
        sg = sendgrid.SendGridAPIClient(api_key='')
        response = sg.send(mail)
        print(f"E-mail enviado com status: {response.status_code}")
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

# ============================
#  Rotas principais
# ============================

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Página inicial para login e registro de usuários.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Processamento do formulário de login
        if 'login' in request.form:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            conn.close()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['name']
                return redirect(url_for('download'))

        # Processamento do formulário de registro
        elif 'register' in request.form:
            name = request.form['name']
            hashed_password = generate_password_hash(password)  # Criptografando senha
            conn = get_db_connection()
            conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/download')
def download():
    """
    Página protegida, visível apenas para usuários logados.
    """
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redireciona se não estiver logado

    username = session['username']
    return render_template('download.html', username=username)

@app.route('/logout')
def logout():
    """
    Realiza o logout do usuário, limpando a sessão.
    """
    session.clear()
    return redirect(url_for('index'))

@app.route('/suporte')
def suporte():
    """
    Página de suporte.
    """
    return render_template('suporte.html')

@app.route('/blueprints')
def blueprints():
    """
    Página de blueprints, protegida para usuários logados.
    """
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('blueprints.html')

@app.route('/success')
def success():
    """
    Página de sucesso após o envio do e-mail.
    """
    return render_template('success.html')

# ============================
#  Recuperação de senha
# ============================

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """
    Página para recuperação de senha.
    """
    if request.method == 'POST':
        email = request.form['email']

        # Verifica se o e-mail está cadastrado
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user:
            # Gera token de recuperação
            token = generate_reset_token(user['id'])
            expiry_time = int(time.time()) + 3600  # Token expira em 1 hora

            # Atualiza o token no banco
            conn = get_db_connection()
            conn.execute('UPDATE users SET reset_token = ?, reset_token_expiry = ? WHERE email = ?', 
                         (token, expiry_time, email))
            conn.commit()
            conn.close()

            if send_recovery_email(email, token):
                return redirect(url_for('success'))
            else:
                return redirect(url_for('email_error'))

        return render_template('email_not_found.html')

    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Página para redefinir senha com token.
    """
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE reset_token = ?', (token,)).fetchone()
    conn.close()

    # Verifica se o token é válido e não expirou
    if user and user['reset_token_expiry'] > int(time.time()):
        if request.method == 'POST':
            new_password = request.form['password']
            hashed_password = generate_password_hash(new_password)

            # Atualiza a senha e limpa o token
            conn = get_db_connection() 
            conn.execute('UPDATE users SET password = ?, reset_token = NULL, reset_token_expiry = NULL WHERE id = ?',
                         (hashed_password, user['id']))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))

        return render_template('reset_password.html', token=token)
    
    # Se o token for inválido ou expirado, renderiza a página de erro
    return render_template('token_invalid.html')


@app.route('/email-error')
def email_error():
    """
    Página de erro no envio do e-mail.
    """
    return render_template('email_error.html')

# ============================
#  Inicialização do servidor
# ============================

if __name__ == '__main__':
    app.run(debug=True)
