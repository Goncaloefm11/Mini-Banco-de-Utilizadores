from flask import Flask, jsonify, request, render_template
import sqlite3

#request permite ao flask ler os dados que alguem envia

app = Flask(__name__) #cria a pagina Flask

@app.route("/") #quando alguem entrar em / executa a funçao
def home():
    return render_template("index.html")


@app.route("/users")
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
            "email": user[3]
        })

    return jsonify(resultado) #resultado em json

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    nome = data["nome"]
    idade = int(data["idade"])
    email = data ["email"]

    if not nome :
        return jsonify({
        "mensagem": "Utilizador não definido!"
        })
    elif idade < 16 :
        return jsonify({
        "mensagem": "Utilizador sem idade atingida!"
        })
    

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO users (nome, idade, email)
        VALUES (?, ?, ?)
    """, (nome, idade, email))

    connection.commit()
    connection.close()

    return jsonify({
        "mensagem": "Utilizador criado com sucesso!"
    })

@app.route("/users/<int:user_id>", methods=["DELETE"])
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

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    nome = data["nome"]
    idade = data["idade"]
    email = data ["email"]

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET nome = ?, idade = ?, email = ?
        WHERE id = ?
    """, (nome, idade, email, user_id))

    connection.commit()
    connection.close()

    return jsonify({
        "mensagem": "Utilizador atualizado com sucesso!"
    })

if __name__ == "__main__":
    app.run(debug=True)