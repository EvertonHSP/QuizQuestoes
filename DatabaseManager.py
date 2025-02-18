import os
import sqlite3


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

        # Verifica se o banco existe; se não, cria e inicializa.
        if not os.path.exists(self.db_path):
            print("Banco de dados não encontrado. Criando um novo...")
            self.initialize_database()
        else:
            print("Banco de dados encontrado. Conectando...")

        self.connect()

    def connect(self):
        """Estabelece a conexão com o banco de dados."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")

    def initialize_database(self):
        """Cria as tabelas no banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executescript('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    senha TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS questoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    enunciado TEXT NOT NULL,
                    imagem TEXT NOT NULL UNIQUE,
                    alternativa_a TEXT,
                    alternativa_b TEXT,
                    alternativa_c TEXT,
                    alternativa_d TEXT,
                    alternativa_e TEXT,
                    resposta_correta TEXT,
                    id_prova INTEGER,
                    area TEXT,
                    FOREIGN KEY(id_prova) REFERENCES prova(id_prova)
                );
                CREATE TABLE IF NOT EXISTS historico_usuario (
                    id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_usuario INTEGER NOT NULL,
                    id_questao INTEGER NOT NULL,
                    acerto INTEGER,
                    tempo_resposta INTEGER,
                    erro INTEGER,
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario),
                    FOREIGN KEY(id_questao) REFERENCES questoes(id)
                );
                CREATE TABLE IF NOT EXISTS prova (
                    id_prova INTEGER PRIMARY KEY AUTOINCREMENT,
                    banca TEXT NOT NULL,
                    ano INTEGER,
                    infor TEXT
                );
                CREATE TABLE IF NOT EXISTS embeddings (
                    id_questao INTEGER PRIMARY KEY,
                    vetor BLOB NOT NULL,
                    FOREIGN KEY(id_questao) REFERENCES questoes(id)
                );
            ''')
            print("Banco de dados inicializado com sucesso!")
