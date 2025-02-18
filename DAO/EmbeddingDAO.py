from Models.Embedding import Embedding
import numpy as np
import sqlite3

class EmbeddingDAO:
    def __init__(self, connection):
        self.connection = connection

    def add_embedding(self, id_questao, vetor):
        """Adiciona um embedding ao banco de dados."""
        with self.connection as conn:
            cursor = conn.cursor()
            # Converte o vetor (array NumPy) em bytes
            vetor_bytes = vetor.tobytes()
            # Insere os dados como binários
            cursor.execute(
                "INSERT INTO embeddings (id_questao, vetor) VALUES (?, ?)",
                (id_questao, sqlite3.Binary(vetor_bytes))
            )
            conn.commit()
            
    def get_embedding_by_questao(self, id_questao):
        print("def get_embedding_by_questao(self, id_questao):...")
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_questao, vetor FROM embeddings WHERE id_questao = ?", (id_questao,)
            )
            data = cursor.fetchone()
            if data:
                id_questao, vetor_bytes = data
                vetor_array = np.frombuffer(vetor_bytes, dtype=np.float32)  # Converte bytes para array NumPy
                return Embedding(id_questao=id_questao, vetor=vetor_array)
            return None

    def get_embeddings_by_area(self, area):
        print("def get_embeddings_by_area(self, area):...")
        """
        Retorna uma lista de questões de uma área específica.
        """
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id_questao, e.vetor
                FROM embeddings e
                JOIN questoes q ON e.id_questao = q.id
                WHERE q.area = ?
            """, (area,))
            embeddings = []
            for row in cursor.fetchall():
                id_questao, vetor_bytes = row

                # Certifique-se de que estamos lidando com bytes e não com texto
                if isinstance(vetor_bytes, bytes):  # Verifique se o dado é do tipo esperado
                    vetor_array = np.frombuffer(vetor_bytes, dtype=np.float32)
                    embeddings.append(Embedding(id_questao=id_questao, vetor=vetor_array))
                else:
                    print(f"Erro: o vetor não é do tipo 'bytes', tipo recebido: {type(vetor_bytes)}")
            return embeddings

            
    def get_all_embeddings(self):
        """Retorna todos os embeddings do banco de dados."""
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_questao, vetor FROM embeddings")
            rows = cursor.fetchall()

            embeddings = []

            for row in rows:
                id_questao, vetor_bytes = row

                # Verifique se vetor_bytes é realmente do tipo 'bytes'
                if isinstance(vetor_bytes, bytes):
                    try:
                        vetor_array = np.frombuffer(vetor_bytes, dtype=np.float32)  # Converte bytes para array NumPy
                        print("Formato de vetor_array:", vetor_array.shape)  # Deve ser (384,) ou outro formato esperado
                        embeddings.append(Embedding(id_questao=id_questao, vetor=vetor_array))
                    except Exception as e:
                        print(f"Erro ao converter vetor para numpy array: {e}")
                else:
                    print(f"Erro: vetor não é do tipo 'bytes', tipo recebido: {type(vetor_bytes)}")

            return embeddings
