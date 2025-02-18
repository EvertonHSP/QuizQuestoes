from Models.Questao import Questao


class QuestaoDAO:
    def __init__(self, connection):
        self.connection = connection

    def get_all_questoes(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, enunciado, imagem, alternativa_a, alternativa_b, "
                "alternativa_c, alternativa_d, alternativa_e, "
                "resposta_correta, area, id_prova FROM questoes"
            )
            return [
                Questao(
                    id_questao=id,
                    enunciado=enunciado,
                    imagem=imagem,
                    alternativas={"A": a, "B": b, "C": c, "D": d, "E": e},
                    resposta_correta=resposta_correta,
                    area=area,
                    id_prova=id_prova
                )
                for id, enunciado, imagem, a, b, c, d, e, resposta_correta, area, id_prova in cursor.fetchall()
            ]

    def get_questao_by_id(self, questao_id):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, enunciado, imagem, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e, resposta_correta, area, id_prova FROM questoes WHERE id = ?",
                (questao_id,)
            )
            data = cursor.fetchone()

            if data:
                id_questao, enunciado, imagem, alt_a, alt_b, alt_c, alt_d, alt_e, resposta_correta, area, id_prova = data

                # Criando um dicionário para as alternativas
                alternativas = {
                    "A": alt_a,
                    "B": alt_b,
                    "C": alt_c,
                    "D": alt_d,
                    "E": alt_e,
                }

                return Questao(id_questao, enunciado, imagem, alternativas, resposta_correta, area, id_prova)
            return None
