import sqlite3

# Conectar ao banco de dados (criar se não existir)
conexao = sqlite3.connect('users.db')

# Criar um cursor para executar comandos SQL
cursor = conexao.cursor()

# Criação da tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    reset_token TEXT,
    reset_token_expiry INTEGER
)
''')

# Confirmar as alterações no banco de dados
conexao.commit()

# Fechar o cursor e a conexão com o banco de dados
cursor.close()
conexao.close()
