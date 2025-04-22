# 🔐 Sistema de Login e Recuperação de Senha com Flask

Este projeto é um sistema web para **login**, **registro de utilizadores** e **recuperação de senha** via e-mail, utilizando **Flask**, **SQLite** e **SendGrid**.

---

## ✨ Funcionalidades

- Cadastro de novos usuários.
- Autenticação de login com verificação segura de senha.
- Download de conteúdos exclusivos para utilizadores logados.
- Recuperação de senha por e-mail com geração de token único.
- Redefinição de senha segura através de link enviado ao e-mail.
- Páginas de suporte e blueprints disponíveis após login.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Flask** 3.0.0
- **Werkzeug** 3.0.1
- **SendGrid** 6.10.0
- **SQLite** (Base de dados)
- **HTML5**, **CSS3**, **JavaScript**

---

## 📁 Estrutura do Projeto

```plaintext
📦 Projeto/
├── static/
│   ├── css/
│   │   ├── download.css
│   │   ├── index.css
│   │   ├── pass.css
│   │   └── suporte.css
│   ├── images/
│   │   └── horror.png
│   └── js/
│       └── index.js
├── templates/
│   ├── blueprints.html
│   ├── download.html
│   ├── email_error.html
│   ├── email_not_found.html
│   ├── forgot_password.html
│   ├── index.html
│   ├── reset_password.html
│   ├── success.html
│   ├── suporte.html
│   └── token_invalid.html
├── app.py
├── create.py
├── requirements.txt
└── users.db
```

---

## 🛠️ Tecnologias

- Python 3.x
- Flask 3.0.0
- Werkzeug 3.0.1
- SendGrid 6.10.0
- SQLite
- HTML5 / CSS3 / JavaScript

---

## ⚙️ Instalação Rápida
## ⚙️ Instalação Rápida

No Windows:

```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
No Linux/Mac:
```
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
No app.py, substitua:
```
sg = sendgrid.SendGridAPIClient(api_key='SUA_API_KEY_AQUI')
```
Ligar o Servidor
```
python app.py
```
