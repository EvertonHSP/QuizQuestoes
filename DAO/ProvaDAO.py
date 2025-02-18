from Models.Prova import Prova


class ProvaDAO:
    def __init__(self, connection):
        self.connection = connection

    def get_provas(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM prova")
        return [Prova(*data) for data in cursor.fetchall()]

    def add_prova(self, banca, ano, infor):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO prova (banca, ano, infor) VALUES (?, ?, ?)",
            (banca, ano, infor))
        self.connection.commit()

    def get_prova_by_id(self, id_prova):
        """Busca uma prova pelo seu ID."""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id_prova, banca, ano, infor FROM prova WHERE id_prova = ?",
            (id_prova,)
        )
        data = cursor.fetchone()
        if data:
            return Prova(*data)  # Retorna um objeto Prova
        return None  # Retorna None se a prova não for encontrada
