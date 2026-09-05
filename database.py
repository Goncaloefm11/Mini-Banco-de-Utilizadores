import sqlite3

connection = sqlite3.connect("database.db") #cria/abre a nossa base de dados

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    email TEXT NOT NULL
)
""")

cursor.execute("""
INSERT INTO users (nome, idade, email)
VALUES (?, ?, ?)
""", ("João", 23, "joao@gmail.com"))

cursor.execute("""
INSERT INTO users (nome, idade, email)
VALUES (?, ?, ?)
""", ("Maria", 21, "maria@gmail.com"))

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