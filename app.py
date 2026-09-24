from flask import Flask, jsonify, request, render_template
import sqlite3

from flask_cors import CORS
from pydantic import BaseModel

#request permite ao flask ler os dados que alguem envia

app = Flask(__name__) #cria a pagina Flask
CORS(app)

def atualizar_base_dados():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    colunas = cursor.execute("PRAGMA table_info(users)").fetchall()
    nomes_colunas = [coluna[1] for coluna in colunas]

    if "cargo" not in nomes_colunas:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN cargo TEXT NOT NULL DEFAULT 'auxiliar'
        """)

    cursor.execute("""
    UPDATE users
    SET cargo = 'chefe'
    WHERE nome = 'João'
    """)

    cursor.execute("""
        UPDATE users
        SET cargo = 'sub-chefe'
        WHERE nome = 'Maria'
    """)

    connection.commit()
    connection.close()


atualizar_base_dados()

@app.route("/") #quando alguem entrar em / executa a funçao
def home():
    return render_template("index.html")


class Utilizador (BaseModel):
    nome : str
    idade : int
    email : str
    cargo : str


@app.get("/users")
def users():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    utilizadores = cursor.fetchall()

    connection.close()

    resultado = []

    for user in utilizadores:
        resultado.append({
            "id": user[0],
            "nome": user[1],
            "idade": user[2],
            "email": user[3],
            "cargo": user[4]
        })

    return jsonify(resultado) #resultado em json

@app.post("/users")
def create_user():
    data = request.get_json()

    nome = data["nome"]
    idade = int(data["idade"])
    email = data ["email"]
    cargo = data["cargo"]
    cargos_validos = ["chefe", "sub-chefe", "auxiliar"]

    if not nome :
        return jsonify({
        "mensagem": "Utilizador não definido!"
        })
    elif idade < 18 :
        return jsonify({
        "mensagem": "Utilizador sem idade atingida!"
        })
    elif cargo not in cargos_validos:
        return jsonify({
            "mensagem": "Cargo inválido!"
        }), 400
    

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO users (nome, idade, email, cargo)
        VALUES (?, ?, ?, ?)
    """, (nome, idade, email, cargo))

    connection.commit()
    connection.close()

    return jsonify({
        "mensagem": "Utilizador criado com sucesso!"
    })

@app.delete("/users/<int:user_id>")
def delete_user(user_id):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id = ?
    """, (user_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "mensagem": "Utilizador eliminado com sucesso!"
    })

@app.put("/users/<int:user_id>")
def update_user(user_id):
    data = request.get_json()

    nome = data["nome"]
    idade = data["idade"]
    email = data ["email"]
    cargo = data ["cargo"]

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET nome = ?, idade = ?, email = ?, cargo = ?
        WHERE id = ?
    """, (nome, idade, email, cargo, user_id))

    connection.commit()
    connection.close()

    return jsonify({
        "mensagem": "Utilizador atualizado com sucesso!"
    })

if __name__ == "__main__":
    app.run(debug=True)