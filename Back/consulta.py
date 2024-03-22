from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@dmlogSYS1",
    database="sys"
)

if conexao.is_connected():
    cursor = conexao.cursor(dictionary=True)
else:
    print("Falha na conexão ao MySQL")

@app.route('/reservas', methods=['GET'])
def obter_reservas():
    cpf = request.args.get('cpf')

    if not cpf:
        return jsonify({"error": "CPF não fornecido"}), 400

    try:
        consulta = f"SELECT ID, DESC_QUARTO, DT_INI_RESERVA, DT_FIM_RESERVA FROM TB_RESERVA WHERE CPF = '{cpf}'"
        cursor.execute(consulta)

        reservas = cursor.fetchall()
        return jsonify(reservas)

    except mysql.connector.Error as erro:
        print("Erro ao executar a consulta:", erro)
        return jsonify({"error": "Erro ao obter as reservas"}), 500

@app.route('/excluir_reserva/<int:reserva_id>', methods=['DELETE'])
def excluir_reserva(reserva_id):
    try:
        consulta = f"DELETE FROM TB_RESERVA WHERE ID = {reserva_id}"
        cursor.execute(consulta)
        conexao.commit()
        return jsonify({"message": "Reserva excluída com sucesso!"}), 200
    except mysql.connector.Error as erro:
        print("Erro ao excluir a reserva:", erro)
        return jsonify({"error": "Erro ao excluir a reserva"}), 500

if __name__ == '__main__':
    app.secret_key = '@dmlogSYS1'
    app.run(debug=True, port=8083)