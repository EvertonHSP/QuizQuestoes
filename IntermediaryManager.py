import logging
import torch
from datetime import datetime
from DatabaseManager import DatabaseManager
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import pytorch_cos_sim
import numpy as np
import random
from DAO import UsuarioDAO, QuestaoDAO
from DAO import HistoricoUsuarioDAO, EmbeddingDAO, ProvaDAO


class IntermediaryManager:

    def __init__(self, db_path):
        self.db_manager = DatabaseManager(db_path)
        self.connection = self.db_manager.connection  # Passa a conexão correta

        # Inicializa os DAOs com a mesma conexão
        self.usuario_dao = UsuarioDAO(self.connection)
        self.questao_dao = QuestaoDAO(self.connection)
        self.historico_dao = HistoricoUsuarioDAO(self.connection)
        self.embedding_dao = EmbeddingDAO(self.connection)
        self.prova_dao = ProvaDAO(self.connection)

        # Carregar modelo de embeddings (se necessário)
        self.model = None
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logging.info("Modelo SentenceTransformer carregado com sucesso.")
        except Exception as e:
            logging.error(
                "Erro ao carregar o modelo SentenceTransformer: %s", str(e))
            raise

    def calcular_desempenho(self, id_usuario):
        print("Processando def calcular_desempenho...", id_usuario)
        nome_usuario = self.usuario_dao.get_user_by_id(id_usuario).nome
        """Calcula o desempenho do usuário com base no histórico."""
        historico = self.historico_dao.get_historico_by_usuario(id_usuario)
        if not historico:
            return f"Usuário {nome_usuario} ainda não respondeu nenhuma questão."

        # Cálculo do desempenho geral
        total_acertos = sum(1 for h in historico if h.acerto == 1)
        total_erros = sum(1 for h in historico if h.erro == 1)
        total_respostas = total_acertos + total_erros
        porcentagem_acertos = (total_acertos / total_respostas) * \
            100 if total_respostas > 0 else 0

        # Classificação geral
        if porcentagem_acertos >= 80:
            classificacao = "Bom"
        elif 50 <= porcentagem_acertos < 80:
            classificacao = "Médio"
        else:
            classificacao = "Ruim"

        # Cálculo do desempenho por área
        desempenho_por_area = {}
        for h in historico:
            if h.area not in desempenho_por_area:
                desempenho_por_area[h.area] = {"acertos": 0, "erros": 0}
            if h.acerto == 1:
                desempenho_por_area[h.area]["acertos"] += 1
            else:
                desempenho_por_area[h.area]["erros"] += 1

        # Calcula a porcentagem de acertos por área
        for area, dados in desempenho_por_area.items():
            total_area = dados["acertos"] + dados["erros"]
            porcentagem_acertos_area = (
                dados["acertos"] / total_area) * 100 if total_area > 0 else 0
            desempenho_por_area[area]["porcentagem_acertos"] = porcentagem_acertos_area

        # Encontra a área com melhor e pior desempenho
        melhor_area = max(desempenho_por_area.items(
        ), key=lambda x: x[1]["porcentagem_acertos"], default=None)
        pior_area = min(desempenho_por_area.items(),
                        key=lambda x: x[1]["porcentagem_acertos"], default=None)

        # Análise temporal do desempenho
        desempenho_por_data = {}
        for h in historico:
            data = datetime.strptime(h.dataTime, "%Y-%m-%d %H:%M:%S.%f").date()
            if data not in desempenho_por_data:
                desempenho_por_data[data] = {"acertos": 0, "erros": 0}
            if h.acerto == 1:
                desempenho_por_data[data]["acertos"] += 1
            else:
                desempenho_por_data[data]["erros"] += 1

        # Calcula a porcentagem de acertos por data
        for data, dados in desempenho_por_data.items():
            total_data = dados["acertos"] + dados["erros"]
            porcentagem_acertos_data = (
                dados["acertos"] / total_data) * 100 if total_data > 0 else 0
            desempenho_por_data[data]["porcentagem_acertos"] = porcentagem_acertos_data

        # Formata a mensagem de desempenho

        mensagem = (
            f"Desempenho do Usuário {nome_usuario}:\n"
            f"  - Total de Respostas: {total_respostas}\n"
            f"  - Acertos: {total_acertos} ({porcentagem_acertos:.2f}%)\n"
            f"  - Classificação Geral: {classificacao}\n"
        )

        # Adiciona informações sobre as áreas de conhecimento
        if melhor_area and pior_area:
            mensagem += (
                f"\nÁreas de Conhecimento:\n"
                f"  - Melhor Desempenho: {melhor_area[0]} ({melhor_area[1]['porcentagem_acertos']:.2f}% de acertos)\n"
                f"  - Pior Desempenho: {pior_area[0]} ({pior_area[1]['porcentagem_acertos']:.2f}% de acertos)\n"
            )

        # Adiciona informações sobre o desempenho ao longo do tempo
        mensagem += "\nDesempenho ao Longo do Tempo:\n"
        for data, dados in desempenho_por_data.items():
            mensagem += f"  - {data}: {dados['porcentagem_acertos']:.2f}% de acertos\n"

        return mensagem

    def gerar_embeddings(self, sentences):
        """Gera embeddings para uma lista de sentenças."""
        try:
            return self.model.encode(sentences, convert_to_tensor=True)
        except Exception as e:
            logging.error("Erro ao gerar embeddings: %s", str(e))
            raise

        print("Processando def sugerir_questao...",
              area_errada, id_questao_atual, questoes_sugeridas)
        """
        Sugere uma questão similar com base na área e no embedding da questão errada.
        """
        print(" 1. Obter o embedding da questão errada...")

        # 1. Obter o embedding da questão errada
        questao_errada_embedding = self.embedding_dao.get_embedding_by_questao(
            id_questao_atual)
        if questao_errada_embedding is None:
            return None, "Embedding da questão atual não encontrado."

        print("2. Obter embeddings das questões da mesma área...")

        # 2. Obter embeddings das questões da mesma área
        embeddings_data = self.embedding_dao.get_embeddings_by_area(
            area_errada)
        if not embeddings_data:
            return None, "Nenhuma questão disponível na mesma área."

        print("3. Filtrar questões já sugeridas e a questão atual...")

        # 3. Filtrar questões já sugeridas e a questão atual
        questoes_a_excluir = {id_questao_atual} | set(questoes_sugeridas)
        embeddings_data = [
            embedding for embedding in embeddings_data
            if embedding.id_questao not in questoes_a_excluir
        ]
        print("4. Verificar se ainda existem questões disponíveis...")

        # 4. Verificar se ainda existem questões disponíveis
        if not embeddings_data:
            return None, "Nenhuma questão disponível na mesma área."

        print("# 5. Preparar os embeddings para cálculo de similaridade...")
        # 5. Preparar os embeddings para cálculo de similaridade
        print("Tipo de embedding.vetor:", type(embeddings_data[0].vetor))
        print("Formato de embedding.vetor:", embeddings_data[0].vetor.shape if hasattr(
            embeddings_data[0].vetor, 'shape') else "Não é um array NumPy")

        embeddings_array = np.array(
            [np.frombuffer(embedding.vetor, dtype=np.float32)
             for embedding in embeddings_data]
        )

        questao_errada_tensor = torch.tensor(
            np.frombuffer(questao_errada_embedding.vetor, dtype=np.float32),
            dtype=torch.float32
        ).unsqueeze(0)
        embeddings_tensor = torch.tensor(embeddings_array, dtype=torch.float32)

        print("Forma de questao_errada_tensor:", questao_errada_tensor.shape)
        print("Forma de embeddings_tensor:", embeddings_tensor.shape)

        print("6. Calcular similaridade do cosseno...")

        try:
            # 6. Calcular similaridade do cosseno
            similaridades = pytorch_cos_sim(
                questao_errada_tensor, embeddings_tensor
            )[0]

            print("Similaridades calculadas:", similaridades)

            print("7. Encontrar a questão mais similar...")

            # 7. Encontrar a questão mais similar
            indice_mais_similar = similaridades.argmax().item()
            id_similar = embeddings_data[indice_mais_similar].id_questao

            print("8. Recuperar a questão sugerida...")

            # 8. Recuperar a questão sugerida
            questao_sugerida = self.questao_dao.get_questao_by_id(id_similar)
            if not questao_sugerida:
                return None, "Questão sugerida não encontrada."

            print("return id_similar, questao_sugerida...")

            return id_similar, questao_sugerida

        except Exception as e:
            print(f"Erro durante o cálculo de similaridade: {e}")
            return None, f"Erro ao calcular similaridade: {e}"

    def registrar_resposta(self, id_usuario, id_questao, acerto_erro, hora_atual, area_questao):
        erro = 1 - acerto_erro
        print("def registrar_resposta...", id_usuario,
              id_questao, acerto_erro, hora_atual, erro)
        self.historico_dao.add_historico(
            id_usuario, id_questao, acerto_erro, hora_atual, erro, area_questao
        )

    def adicionar_usuario(self, nome, email, senha):
        """Adiciona um novo usuário."""
        self.usuario_dao.add_user(nome, email, senha)

    def autenticar_usuario(self, email, senha):
        """Autentica um usuário."""
        usuario = self.usuario_dao.get_user_by_email(email)
        if usuario and usuario.senha == senha:
            return usuario.id_usuario
        return None

    def enviar_questao_aleatoria(self):
        print("Processando def enviar_questao_aleatoria")
        """Retorna uma questão aleatória do banco de dados."""
        questoes = self.questao_dao.get_all_questoes()
        if not questoes:
            return None, "Nenhuma questão disponível no banco de dados."
        questao_aleatoria = random.choice(questoes)
        return questao_aleatoria

    def sugerir_questao(self, area_errada, id_questao_atual, questoes_sugeridas):
        print("Processando def sugerir_questao...",
              area_errada, id_questao_atual, questoes_sugeridas)
        """
        Sugere uma questão similar com base na área e no embedding da questão errada.
        """
        # print(" 1. Obter o embedding da questão errada...")
        # 1. Obter o embedding da questão errada
        questao_errada_embedding = self.embedding_dao.get_embedding_by_questao(
            id_questao_atual)
        if questao_errada_embedding is None:
            return None, "Embedding da questão atual não encontrado."

        # print("2. Obter embeddings das questões da mesma área...")
        # 2. Obter embeddings das questões da mesma área
        embeddings_data = self.embedding_dao.get_embeddings_by_area(
            area_errada)

        # print("3. Filtrar questões já sugeridas e a questão atual...")
        # 3. Filtrar questões já sugeridas e a questão atual
        questoes_a_excluir = {id_questao_atual} | set(questoes_sugeridas)

        if not embeddings_data or all(embedding.id_questao in questoes_a_excluir for embedding in embeddings_data):
            print("Nenhuma questão encontrada na área, buscando em todas as áreas...")
            embeddings_data = self.embedding_dao.get_all_embeddings()

        embeddings_data = [
            embedding for embedding in embeddings_data
            if embedding.id_questao not in questoes_a_excluir
        ]

        # print("# 4. Preparar os embeddings para cálculo de similaridade...")
        # 5. Preparar os embeddings para cálculo de similaridade
        embeddings_array = np.array(
            [embedding.vetor for embedding in embeddings_data]  # Já é um array NumPy
        )

        questao_errada_tensor = torch.tensor(
            questao_errada_embedding.vetor,  # Já é um array NumPy
            dtype=torch.float32).unsqueeze(0)
        embeddings_tensor = torch.tensor(embeddings_array, dtype=torch.float32)

       # """ print("Forma de questao_errada_tensor:", questao_errada_tensor.shape)
        # print("Forma de embeddings_tensor:", embeddings_tensor.shape)"""

        # print("5. Normalizar os embeddings...")
        # 6. Normalizar os embeddings
        questao_errada_tensor = torch.nn.functional.normalize(
            questao_errada_tensor, p=2, dim=1)
        embeddings_tensor = torch.nn.functional.normalize(
            embeddings_tensor, p=2, dim=1)

        # print("6. Calcular similaridade do cosseno...")

        try:
            similaridades = torch.nn.functional.cosine_similarity(
                questao_errada_tensor.detach().cpu(),
                embeddings_tensor.detach().cpu())

            print("Similaridades calculadas:", similaridades)

            # print("7. Encontrar a questão mais similar...")

            # 8. Encontrar a questão mais similar
            indice_mais_similar = similaridades.argmax().item()
            id_similar = embeddings_data[indice_mais_similar].id_questao

            print("8. Recuperar a questão sugerida...", id_similar)

            # 9. Recuperar a questão sugerida
            questao_sugerida = self.questao_dao.get_questao_by_id(id_similar)
            if not questao_sugerida:
                return None, "Questão sugerida não encontrada."

            # print("return id_similar, questao_sugerida...")

            return id_similar, questao_sugerida

        except Exception as e:
            print(f"Erro durante o cálculo de similaridade: {e}")
            return None

    def get_prova_by_id(self, id_prova):
        return self.prova_dao.get_prova_by_id(id_prova)
