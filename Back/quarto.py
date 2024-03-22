from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app, resources={r"/cadastrar_quarto": {"origins": "*"}})

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

# Rota para inserir um novo quarto
@app.route('/cadastrar_quarto', methods=['POST'])
def cadastrar_quarto():
    data = request.json
    descricao = data.get('descricao')
    valor = data.get('valor')

    # Verifica se todos os campos foram fornecidos
    if not descricao or not valor:
        return jsonify({'success': False, 'message': 'Descrição e valor do quarto são obrigatórios'}), 400

    # Conecta ao banco de dados
    db = connect_to_database()
    if db is None:
        return jsonify({'success': False, 'message': 'Erro ao conectar ao banco de dados'}), 500

    cursor = db.cursor()

    try:
        # Executa a inserção do novo quarto na tabela
        query = "INSERT INTO TB_QUARTO (DESC_QUARTO, VLR_NOITE) VALUES (%s, %s)"
        cursor.execute(query, (descricao, valor))
        db.commit()  # Confirma a transação

        # Verifica o resultado da inserção
        if cursor.rowcount > 0:
            return jsonify({'success': True, 'message': 'Quarto cadastrado com sucesso'})
        else:
            return jsonify({'success': False, 'message': 'Nenhum quarto foi cadastrado'}), 500
    except mysql.connector.Error as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        db.rollback()  # Reverte a transação em caso de erro
        return jsonify({'success': False, 'message': 'Erro ao cadastrar o quarto'}), 500
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True, port=8081)