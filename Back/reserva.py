from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app, resources={r"/quartos": {"origins": "*"}})

def obter_quartos(data_entrada, data_saida):
    # Estabelecer conexão com o banco de dados MySQL
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@dmlogSYS1",
        database="sys"
    )

    # Verificar se a conexão foi estabelecida
    if conexao.is_connected():
        # Criar um cursor para executar consultas
        cursor = conexao.cursor()

        try:
            # Consulta SQL para obter os quartos disponíveis entre as datas de entrada e saída
            consulta = f"SELECT B.DESC_QUARTO FROM TB_QUARTO B WHERE NOT EXISTS ( SELECT NULL FROM TB_RESERVA A WHERE A.DESC_QUARTO = B.DESC_QUARTO AND (('{data_entrada}' BETWEEN A.DT_INI_RESERVA AND A.DT_FIM_RESERVA) OR ('{data_saida}' BETWEEN A.DT_INI_RESERVA AND A.DT_FIM_RESERVA) OR (A.DT_INI_RESERVA BETWEEN '{data_entrada}' AND '{data_saida}'))) ORDER BY B.DESC_QUARTO ASC"
            cursor.execute(consulta)

            # Obter todos os resultados da consulta
            resultados = cursor.fetchall()

            # Transformar os resultados em uma lista
            quartos = [resultado[0] for resultado in resultados]

            return quartos

        except mysql.connector.Error as erro:
            print("Erro ao executar a consulta:", erro)

        finally:
            # Fechar o cursor e a conexão
            if cursor:
                cursor.close()
            conexao.close()

    else:
        print("Falha na conexão ao MySQL")

def inserir_reserva(quarto, data_entrada, data_saida, cpf):
    # Estabelecer conexão com o banco de dados MySQL
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@dmlogSYS1",
        database="sys"
    )

    # Verificar se a conexão foi estabelecida
    if conexao.is_connected():
        # Criar um cursor para executar consultas
        cursor = conexao.cursor()

        try:
            # Consulta SQL para inserir a reserva
            consulta = f"INSERT INTO TB_RESERVA (DESC_QUARTO, DT_INI_RESERVA, DT_FIM_RESERVA, CPF) VALUES ('{quarto}', '{data_entrada}', '{data_saida}', '{cpf}')"
            cursor.execute(consulta)

            # Confirmar a inserção
            conexao.commit()

            return True

        except mysql.connector.Error as erro:
            print("Erro ao inserir a reserva:", erro)
            return False

        finally:
            # Fechar o cursor e a conexão
            if cursor:
                cursor.close()
            conexao.close()

    else:
        print("Falha na conexão ao MySQL")
        return False

@app.route('/quartos', methods=['GET', 'POST'])
def handle_quartos():
    if request.method == 'GET':
        data_entrada = request.args.get('dataEntrada')
        data_saida = request.args.get('dataSaida')
        cpf = request.args.get('cpf')

        if not data_entrada or not data_saida:
            return jsonify({"error": "Data de entrada ou data de saída não fornecida"}), 400

        quartos = obter_quartos(data_entrada, data_saida)
        return jsonify(quartos)

    elif request.method == 'POST':
        data = request.get_json()
        quarto = data.get('quarto')
        data_entrada = data.get('dataEntrada')
        data_saida = data.get('dataSaida')
        cpf = data.get('cpf')

        if not quarto or not data_entrada or not data_saida or not cpf:
            return jsonify({"error": "Dados incompletos para realizar a reserva"}), 400

        if inserir_reserva(quarto, data_entrada, data_saida, cpf):
            return jsonify({"message": "Reserva realizada com sucesso"}), 201
        else:
            return jsonify({"error": "Erro ao realizar a reserva"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8082)