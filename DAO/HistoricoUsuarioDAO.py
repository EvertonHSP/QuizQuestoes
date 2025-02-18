from Models.HistoricoUsuario import HistoricoUsuario


class HistoricoUsuarioDAO:
    def __init__(self, connection):
        self.connection = connection

    def add_historico(self, id_usuario, id_questao, acerto, hora_atual, erro, area_questao):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                (
                    "INSERT INTO historico_usuario (id_usuario, id_questao,"
                    " acerto, dataTime, erro, area) VALUES (?, ?, ?, ?, ?, ?)"
                ),
                (id_usuario, id_questao, acerto, hora_atual, erro, area_questao),
            )
            conn.commit()


    def get_historico_by_usuario(self, id_usuario):
        """Retorna o histórico de um usuário."""
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_usuario, id_questao, acerto, dataTime, erro, id_historico, area "
                "FROM historico_usuario WHERE id_usuario = ?",
                (id_usuario,)
            )
            return [HistoricoUsuario(*data) for data in cursor.fetchall()]

    def alterar_erro(self, id_usuario, id_questao, novo_erro):
        """


        :param id_usuario: ID do usuário.
        :param id_questao: ID da questão.
        :param novo_erro: Novo valor para o campo 'erro'.
        """
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE historico_usuario
                SET erro = ?
                WHERE id_usuario = ? AND id_questao = ?
                """,
                (novo_erro, id_usuario, id_questao),
            )
            conn.commit()


    def alterar_acerto(self, id_usuario, id_questao, novo_acerto):
        """


        :param id_usuario: ID do usuário.
        :param id_questao: ID da questão.
        :param novo_acerto: Novo valor para o campo 'acerto'.
        """
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE historico_usuario
                SET acerto = ?
                WHERE id_usuario = ? AND id_questao = ?
                """,
                (novo_acerto, id_usuario, id_questao),
            )
            conn.commit()
