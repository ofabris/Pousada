from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configuração da conexão com o banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '@dmlogSYS1',
    'database': 'sys'
}

# Função para conectar ao banco de dados
def connect_to_database():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Rota para verificar o login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Verifica se os dados de login foram fornecidos
    if not username or not password:
        return jsonify({'success': False, 'message': 'Nome de usuário ou senha ausentes'}), 400

    # Conecta ao banco de dados
    db = connect_to_database()
    if db is None:
        return jsonify({'success': False, 'message': 'Erro ao conectar ao banco de dados'}), 500

    cursor = db.cursor()

    try:
        # Executa a consulta SQL para verificar o login
        query = "SELECT ID FROM TB_USUARIO WHERE NOME = %s AND SENHA = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            # Salva o ID do usuário na sessão
            session['usuario_id'] = result[0]
            return jsonify({'success': True, 'message': 'Login bem-sucedido'})
        else:
            return jsonify({'success': False, 'message': 'Nome de usuário ou senha incorretos'}), 401
    except mysql.connector.Error as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        return jsonify({'success': False, 'message': 'Erro ao verificar o login'}), 500
    finally:
        cursor.close()
        db.close()

# Rota para cadastrar um novo usuário
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    nome = data.get('nome')
    telefone = data.get('telefone')
    cpf = data.get('cpf')
    data_nascimento = data.get('dataNascimento')
    senha = data.get('senha')

    # Verifica se todos os campos foram fornecidos
    if not nome or not telefone or not cpf or not data_nascimento or not senha:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'}), 400

    # Conecta ao banco de dados
    db = connect_to_database()
    if db is None:
        return jsonify({'success': False, 'message': 'Erro ao conectar ao banco de dados'}), 500

    cursor = db.cursor()

    try:
        # Executa a inserção do novo usuário na tabela
        query = "INSERT INTO TB_USUARIO (nome, telefone, cpf, data_nascimento, senha) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, telefone, cpf, data_nascimento, senha))
        db.commit()  # Confirma a transação

        # Verifica o resultado da inserção
        if cursor.rowcount > 0:
            return jsonify({'success': True, 'message': 'Usuário cadastrado com sucesso'})
        else:
            return jsonify({'success': False, 'message': 'Nenhum usuário foi cadastrado'}), 500
    except mysql.connector.Error as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        db.rollback()  # Reverte a transação em caso de erro
        return jsonify({'success': False, 'message': 'Erro ao cadastrar o usuário'}), 500
    finally:
        cursor.close()
        db.close()
        
if __name__ == '__main__':
    app.secret_key = '@dmlogSYS1'
    app.run(debug=True, port=8080)