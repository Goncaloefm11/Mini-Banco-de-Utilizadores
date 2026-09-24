import sqlite3

connection = sqlite3.connect("database.db") #cria/abre a nossa base de dados

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    email TEXT NOT NULL,
    cargo TEXT NOT NULL DEFAULT "auxiliar"
)
""")

cursor.execute("""
INSERT INTO users (nome, idade, email, cargo)
VALUES (?, ?, ?, ?)
""", ("João", 23, "joao@gmail.com", "chefe"))

cursor.execute("""
INSERT INTO users (nome, idade, email, cargo)
VALUES (?, ?, ?, ?)
""", ("Maria", 21, "maria@gmail.com", "sub-chefe"))

cursor.execute("""
INSERT INTO users (nome, idade, email)
VALUES (?, ?, ?)
""", ("Goncalo", 22, "goncalo@gmail.com"))

# cursor.execute("""
# DELETE FROM users
# WHERE nome = ?
# """, ("Gonçalo",))

connection.commit()
connection.close()

print("Base de dados criada e utilizadores adicionados")