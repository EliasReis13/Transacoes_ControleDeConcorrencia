import sqlite3

def setup_database():
    # Conecta ao banco de dados SQLite
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Cria a tabela de contas se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        )
    ''')

    # Insere algumas contas com saldos iniciais
    cursor.execute('INSERT OR IGNORE INTO accounts (name, balance) VALUES (?, ?)', ('João', 5000.0))
    cursor.execute('INSERT OR IGNORE INTO accounts (name, balance) VALUES (?, ?)', ('Maria', 8000.0))
    cursor.execute('INSERT OR IGNORE INTO accounts (name, balance) VALUES (?, ?)', ('Pedro', 9000.0))
    cursor.execute('INSERT OR IGNORE INTO accounts (name, balance) VALUES (?, ?)', ('Matheus', 6000.0))
    cursor.execute('INSERT OR IGNORE INTO accounts (name, balance) VALUES (?, ?)', ('Paulo', 7000.0))
    cursor.execute('INSERT OR IGNORE INTO accounts (name, balance) VALUES (?, ?)', ('Caio', 10000.0))
    cursor.execute('INSERT OR IGNORE INTO accounts (name, balance) VALUES (?, ?)', ('Lucas', 90000.0))

    # Confirma as mudanças e fecha a conexão
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_database()
